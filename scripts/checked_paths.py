"""Inspect regular files and directories without following links or reparse points."""
import os
from pathlib import Path
import stat


def metadata(path):
    """Inspect a filesystem entry before reading it. Check Windows raw attributes first."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        getter = ctypes.WinDLL("kernel32", use_last_error=True).GetFileAttributesW
        getter.argtypes = (wintypes.LPCWSTR,)
        getter.restype = wintypes.DWORD
        attrs = getter(str(path))
        if attrs == 0xFFFFFFFF:
            raise ctypes.WinError(ctypes.get_last_error())
        if attrs & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Linked path is unsupported: {path}")
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode):
        raise ValueError(f"Linked path is unsupported: {path}")
    return info

def directory(path):
    # Windows exposes a UNC share anchor as a namespace, not a file entry.
    for part in (*reversed(path.parents), path):
        if os.name == "nt" and part == Path(part.anchor) and part.drive.startswith("\\\\"):
            if part == path:
                raise ValueError("Choose a project directory below the UNC share.")
            continue
        if not stat.S_ISDIR(metadata(part).st_mode):
            raise ValueError(f"Expected an existing directory: {part}")

def existing_file(path):
    try:
        mode = metadata(path).st_mode
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(mode):
        raise ValueError(f"Expected a regular file: {path}")
    return path.read_bytes()
