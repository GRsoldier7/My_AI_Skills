# Agency roster and staging builder

Canonical personas: `agents/agency/<division>/`. The source is Agency Agents
`b37b5bb33b78f2c1d6567d98e25ca818e3259219`, MIT. `divisions.json` remains the division authority.
The roster is reference material; it is not preloaded as hundreds of skills.

From the repository root, generate into a new staging directory:

```sh
python3 platform-configs/hermes/agency/build-hermes-plugin.py --source-root agents/agency --out /tmp/agency-staging-review
python3 platform-configs/hermes/agency/check-hermes-plugin.py
AGENCY_STAGED_PLUGIN=/tmp/agency-staging-review/agency-agents-router python3 platform-configs/hermes/agency/test-hermes-plugin.py
```

The generator requires explicit source/output paths, preserves existing output,
rejects common live configuration locations, and copies the upstream license.
It never installs the plugin, changes Hermes configuration, starts a service,
or enables tools. The generated README reflects this staging boundary.
The tests use fake lifecycle objects: they spend no model/API credits and do
not start Hermes. Their success is not proof of native-host compatibility.

The optional plugin exposes search, inspect, load, and delegate. Select one
specialist after inspecting its scope; keep the existing Hermes lead in charge.
Runtime activation requires mapping tools and target permissions to the host.
The reviewed lifecycle is in-process: it is not durable restart recovery.
On unconfirmed cancellation/pending state, reconcile the child before retrying;
never run a fallback that could duplicate a still-running task.

Local changes to the upstream builder/tests: explicit staging arguments; no
output deletion; source division-name validation; license inclusion; relocated
source/test paths; staged plugin selection through AGENCY_STAGED_PLUGIN; local
staging documentation. Source bodies and tool schemas are otherwise preserved.
