#!/usr/bin/env python3
"""Package canonical router skills or install them user-wide. Python 3.10+, stdlib only."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

SKILLS = (
    'project-router', 'projectplan-builder', 'projectplan-rescope',
    'continuing-alm-work', 'workbetter', 'clean-project', 'directory-cleanup',
)
START = '<!-- project-router:user-guidance:start -->'
END = '<!-- project-router:user-guidance:end -->'
GUIDANCE = f'''{START}
## Project lifecycle routing
For multi-step project startup, next-step selection, resumption, rescoping,
cleanup, or readiness assessment, use the installed `project-router` skill.
This scoped rule replaces generic always-use-master routing for those requests;
it does not replace task-specific instructions, safety, or approval boundaries.
Keep one controller. An existing owner retains control unless ownership is
explicitly transferred. Do not load both master-orchestrator and project-router
as competing controllers, and do not route standalone questions through either.
Default to read-only assessment without execution authorization. Load only the
selected specialist; never invent skill invocations or verification results.
{END}
'''.encode()


def no_symlinks(path: Path, boundary: Path) -> None:
    """Refuse redirection below the user/source boundary."""
    current = path
    while current != boundary:
        if current.is_symlink():
            raise ValueError(f'Refusing symlink: {current}')
        if current == current.parent:
            raise ValueError(f'Path outside boundary: {path}')
        current = current.parent


def runtime_files(root: Path) -> dict[str, bytes]:
    """Read only the seven skills and their declarative runtime resources."""
    root = root.resolve()
    base = root / 'skills/aarons-latest'
    files: dict[str, bytes] = {}
    for name in SKILLS:
        folder = base / name
        main = folder / 'SKILL.md'
        no_symlinks(main, root)
        text = main.read_text(encoding='utf-8')
        if not re.search(rf'^name:\s*{re.escape(name)}\s*$', text, re.M):
            raise ValueError(f'Skill name does not match directory: {main}')
        if not text.startswith('---\n') or not re.search(r'^description:', text, re.M):
            raise ValueError(f'Missing skill metadata: {main}')
        files[f'{name}/SKILL.md'] = main.read_bytes()
        for directory in ('references', 'agents'):
            sub = folder / directory
            no_symlinks(sub, root)
            if not sub.exists():
                continue
            for path in sorted(sub.rglob('*')):
                no_symlinks(path, root)
                if path.is_file():
                    if path.suffix not in ('.md', '.yaml', '.yml', '.json'):
                        raise ValueError(f'Unreviewed resource type: {path}')
                    files[f'{name}/{path.relative_to(folder).as_posix()}'] = path.read_bytes()
    return files


def build(root: Path, output: Path) -> None:
    """Build a deterministic private plugin ZIP; never overwrite a different file."""
    files = runtime_files(root)
    manifest_path = root / 'platform-configs/openai/project-router/plugin.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('name') != 'project-router' or not re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', '')):
        raise ValueError('Invalid plugin identity/version')
    interface = manifest['extensions']['com.openai']['interface']
    if len(interface['shortDescription']) > 30:
        raise ValueError('Plugin subtitle exceeds 30 characters')
    payload = {f'skills/{name}': data for name, data in files.items()}
    payload['plugin.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    payload['SOURCES.json'] = (json.dumps({
        'repository': 'GRsoldier7/My_AI_Skills',
        'canonical_path': 'skills/aarons-latest',
        'sha256': {name: hashlib.sha256(data).hexdigest() for name, data in sorted(payload.items())},
    }, indent=2) + '\n').encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(payload.items()):
            info = zipfile.ZipInfo(f'project-router/{name}', date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    result = buffer.getvalue()
    if output.is_symlink():
        raise ValueError(f'Refusing symlink output: {output}')
    if output.exists():
        if output.read_bytes() != result:
            raise FileExistsError(f'Refusing to overwrite different archive: {output}')
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as stream:
            stream.write(result)
    print(f'Plugin ZIP: {output} ({len(SKILLS)} skills, {len(payload)} files)')


def install(root: Path, home: Path, *, apply: bool = False, guidance: bool = False) -> None:
    """Preflight all destinations; preserve existing content and never overwrite skills."""
    files = runtime_files(root)
    home = home.expanduser().resolve()
    target = home / '.agents/skills'
    no_symlinks(target, home)
    pending: list[str] = []
    for name in SKILLS:
        dest = target / name
        no_symlinks(dest, home)
        required = {p[len(name) + 1:]: data for p, data in files.items() if p.startswith(name + '/')}
        if dest.exists():
            if not dest.is_dir():
                raise FileExistsError(f'Not a skill directory: {dest}')
            for rel, data in required.items():
                path = dest / rel
                no_symlinks(path, home)
                if not path.is_file() or path.read_bytes() != data:
                    raise FileExistsError(f'Existing skill differs; review/backup it before retrying: {path}')
        else:
            pending.append(name)
    instruction = home / '.codex/AGENTS.md'
    old = b''
    updated = b''
    if guidance:
        custom_home = os.environ.get('CODEX_HOME')
        if custom_home and Path(custom_home).expanduser().resolve() != home / '.codex':
            raise ValueError('Custom CODEX_HOME detected; install without --global-guidance and merge the documented block there.')
        override = home / '.codex/AGENTS.override.md'
        if override.exists() or override.is_symlink():
            instruction = override
        no_symlinks(instruction, home)
        old = instruction.read_bytes() if instruction.exists() else b''
        if START.encode() in old or END.encode() in old:
            if old.count(START.encode()) != 1 or old.count(END.encode()) != 1 or GUIDANCE not in old:
                raise FileExistsError(f'Existing router guidance differs; preserve and reconcile: {instruction}')
            updated = old
        else:
            updated = old + (b'\n\n' if old else b'') + GUIDANCE
    print(f'{"Apply" if apply else "Dry run"}: {len(pending)} new skills; {len(SKILLS)-len(pending)} already match; target={target}')
    if not apply:
        return
    if pending:
        target.mkdir(parents=True, exist_ok=True)
    for name in pending:
        dest = target / name
        with tempfile.TemporaryDirectory(prefix='.project-router-', dir=target) as temp:
            staged = Path(temp) / name
            staged.mkdir()
            for rel, data in files.items():
                if rel.startswith(name + '/'):
                    path = staged / rel[len(name) + 1:]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
            if dest.exists() or dest.is_symlink():
                raise FileExistsError(f'Destination changed during installation: {dest}')
            staged.rename(dest)
    if guidance and updated != old:
        instruction.parent.mkdir(parents=True, exist_ok=True)
        current = instruction.read_bytes() if instruction.exists() else b''
        if current != old:
            raise FileExistsError(f'Instructions changed during installation: {instruction}')
        with tempfile.NamedTemporaryFile(dir=instruction.parent, delete=False) as stream:
            stage = Path(stream.name)
            stream.write(updated)
        try:
            if instruction.exists():
                stage.chmod(instruction.stat().st_mode & 0o777)
            stage.replace(instruction)
        finally:
            stage.unlink(missing_ok=True)
    print('Local installation finished. Restart Codex and confirm $project-router is available. Other devices were not modified.')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('build', 'install'))
    parser.add_argument('--output', type=Path, default=Path('project-router-plugin.zip'))
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--apply', action='store_true', help='Write local user installation; otherwise preview only.')
    parser.add_argument('--global-guidance', action='store_true', help='Append scoped routing guidance without replacing existing instructions.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        if args.action == 'build':
            build(root, args.output)
        else:
            install(root, args.home, apply=args.apply, guidance=args.global_guidance)
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f'Project Router: {error}\n')


if __name__ == '__main__':
    main()
