"""Check the offline work artifact in an installed Chromium browser with WebDriver."""
import json
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "skills/engineering/enterprise-web-artifacts/assets/operations-brief.html"


def request(url, payload=None, method=None, *, timeout=20):
    body = None if payload is None else json.dumps(payload).encode()
    req = Request(url, data=body, method=method, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=timeout) as response:
        return json.load(response)["value"]


def trial(endpoint, browser, width, javascript):
    chrome = {"binary": browser,
              "args": ["--headless=new", "--disable-background-networking", "--remote-debugging-pipe"],
              "prefs": {"profile.managed_default_content_settings.javascript": 1 if javascript else 2}}
    capabilities = {"browserName": "chrome", "goog:chromeOptions": chrome,
                    "goog:loggingPrefs": {"browser": "ALL", "performance": "ALL"}}
    session = request(endpoint + "/session", {"capabilities": {"alwaysMatch": capabilities}}, timeout=70)
    base = endpoint + "/session/" + session["sessionId"]
    def post(path, data):
        return request(base + path, data)
    def evaluate(expression):
        return post("/execute/sync", {"script": "return " + expression, "args": []})
    def cdp(cmd, params):
        return post("/goog/cdp/execute", {"cmd": cmd, "params": params})
    try:
        cdp("Emulation.setDeviceMetricsOverride", {"width": width, "height": 800, "deviceScaleFactor": 1, "mobile": False})
        cdp("Network.enable", {})
        cdp("Network.emulateNetworkConditions", {"offline": True, "latency": 0, "downloadThroughput": 0, "uploadThroughput": 0})
        post("/url", {"url": SAMPLE.as_uri()})
        assert evaluate("document.querySelector('#rate').textContent") == "30%"
        assert evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        assert evaluate("document.querySelectorAll('tbody tr:not([hidden])').length") == 3
        assert evaluate("document.querySelector('#controls').hidden") != javascript
        if javascript:
            def key(value):
                source = {"type": "key", "id": "keyboard", "actions": [
                    {"type": "keyDown", "value": value}, {"type": "keyUp", "value": value}]}
                post("/actions", {"actions": [source]})
            key("\ue004")  # Tab
            assert evaluate("document.activeElement.id") == "area"
            key("\ue010")  # End
            assert evaluate("document.querySelector('#rate').textContent") == "No eligible requests"
            key("\ue013")  # Up from C to B
            assert evaluate("document.querySelector('#rate').textContent") == "25%"
            assert evaluate("document.querySelector('#counts').textContent") == "2 completed · 8 eligible"
            assert evaluate("document.querySelectorAll('tbody tr:not([hidden])').length") == 1
            cdp("Emulation.setEmulatedMedia", {"media": "print"})
            assert evaluate("getComputedStyle(document.querySelector('#controls')).display") == "none"
        for item in post("/se/log", {"type": "performance"}):
            event = json.loads(item["message"])["message"]
            if event["method"] == "Network.requestWillBeSent":
                assert not event["params"]["request"]["url"].startswith(("http:", "https:"))
        assert not [item for item in post("/se/log", {"type": "browser"}) if item["level"] == "SEVERE"]
    finally:
        request(base, method="DELETE")


def main():
    browser = shutil.which("google-chrome") or shutil.which("chromium")
    driver = shutil.which("chromedriver")
    if not browser or not driver:
        raise SystemExit("Install a matching Chrome and ChromeDriver for this optional browser check.")
    with socket.socket() as available:
        available.bind(("127.0.0.1", 0))
        port = available.getsockname()[1]
    endpoint = f"http://127.0.0.1:{port}"
    with tempfile.TemporaryFile() as log:
        with subprocess.Popen([driver, f"--port={port}", "--verbose"],
                              stdout=log, stderr=subprocess.STDOUT) as process:
            try:
                for _ in range(60):
                    try:
                        if request(endpoint + "/status", timeout=1)["ready"]:
                            break
                    except URLError:
                        pass
                    time.sleep(.1)
                else:
                    raise RuntimeError("ChromeDriver did not become ready")
                for width, javascript in ((1280, True), (320, True), (320, False)):
                    print(f"Testing Chrome at {width}px (JavaScript {'on' if javascript else 'off'})", flush=True)
                    trial(endpoint, browser, width, javascript)
            except Exception:
                log.seek(max(0, log.tell() - 12000))
                print(log.read().decode("utf-8", errors="replace"), file=sys.stderr)
                raise
            finally:
                process.terminate()
    print("Chrome passed desktop, mobile, keyboard, print, no-network and JavaScript-off checks.")


if __name__ == "__main__":
    main()
