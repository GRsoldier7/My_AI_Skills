#!/usr/bin/env python3
"""Generate the library index or stage a selected platform bundle; never install it."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('skill_sets', ROOT / 'scripts/skill-sets.py')
sets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sets)
PLATFORMS = ('chatgpt', 'copilot', 'hermes', 'codex')
POLICY = '''## Library delivery boundaries

Use only tools actually available and authorized in this host. Repository/user
instructions govern permissions. This package does not authorize installation,
downloads, MCP setup, hooks, account changes, publication, messaging or deployment.
Select one workflow owner and invoke other specialists only for their assigned
role. Report unavailable checks rather than claiming execution. Keep employer,
client, authentication and session data outside the public skills library.
'''


def read_json(root: Path, relative: str) -> dict:
    return json.loads(sets.safe_path(root, relative).read_text(encoding='utf-8'))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def with_policy(text: str, name: str, instructions: bool = False, prepend: str = "") -> str:
    match = re.match(r'^---\n.*?\n---(?:\n|$)', text, re.S)
    if not match:
        text = f'---\nname: {name}\ndescription: Portable guidance for {name}.\n---\n' + text
        match = re.match(r'^---\n.*?\n---\n', text, re.S)
    extra = '\nInstruction-only delivery: do not invoke local scripts, engines or shell commands. Use available host capabilities; runtime verification is not provided.\n' if instructions else ''
    return text[:match.end()] + '\n' + POLICY + extra + '\n' + prepend + '\n' + text[match.end():]


def load(root: Path) -> tuple[dict, dict, dict]:
    manifest = read_json(root, 'platform-configs/skill-sets/manifest.json')
    sets.validate(root, manifest)
    delivery = read_json(root, 'platform-configs/library-delivery.json')
    inventory = read_json(root, 'platform-configs/artifact-sources.json')
    artifacts = {a['path']: a for a in inventory['artifacts']}
    if len(artifacts) != len(inventory['artifacts']):
        raise ValueError('Duplicate artifact paths')
    for path, record in artifacts.items():
        verified_artifact(root, path, artifacts)
        if record.get('license_path') and not sets.safe_path(root,record['license_path']).is_file():
            raise ValueError(f'Missing artifact license: {path}')
    return manifest, delivery, artifacts


def ensure_output(path: Path, root: Path) -> None:
    if path.exists() or path.is_symlink():
        raise ValueError(f'Output already exists: {path}')
    for parent in path.parents:
        if parent.is_symlink():
            raise ValueError('Output parent is a symlink')
    resolved = path.resolve()
    if resolved.is_relative_to(root.resolve()) and not resolved.is_relative_to((root / '.bundle-cache').resolve()):
        raise ValueError('Stage outside the repository or inside .bundle-cache')


def verified_artifact(root: Path, path: str, records: dict) -> bytes:
    if path not in records:
        raise ValueError(f'Unregistered artifact: {path}')
    data = sets.safe_path(root, path).read_bytes()
    if sha(data) != records[path]['sha256']:
        raise ValueError(f'Artifact changed: {path}')
    return data


def rewrite_links(text: str, resource: Path, source_map: dict[Path, Path], external: dict[Path, str] | None = None) -> str:
    for target in sets.markdown_links(text):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
            continue
        raw, sep, anchor = target.partition('#')
        destination = (resource.parent / raw).resolve()
        if destination in source_map and resource.resolve() in source_map:
            relative = os.path.relpath(source_map[destination], source_map[resource.resolve()].parent).replace(os.sep, '/')
            text = text.replace('](' + target + ')', '](' + relative + (sep + anchor if sep else '') + ')')
        elif external and destination in external:
            text = text.replace('](' + target + ')', '](' + external[destination] + (sep + anchor if sep else '') + ')')
        else:
            raise ValueError(f'Export loses a referenced resource: {resource.name}: {target}')
    return text


def export(root: Path, profile: str, platform: str, output: Path) -> dict:
    manifest, config, artifacts = load(root)
    if platform not in PLATFORMS:
        raise ValueError('Unsupported platform')
    bundle = config['bundles'].get(profile)
    if not bundle or platform not in bundle['platforms']:
        raise ValueError(f'Bundle {profile} is not available for {platform}')
    entries = sets.resolve_profile(manifest, bundle.get('profile', profile))
    selected = []
    source_map: dict[Path, Path] = {}
    payload: dict[str, bytes] = {}
    prefix = {'chatgpt':'skills','copilot':'.github/skills','hermes':'skills','codex':'.agents/skills'}[platform]
    for entry in entries:
        policy = config.get('skills', {}).get(entry['id'], {}).get(platform, {})
        mode = policy.get('mode', 'full')
        if mode == 'blocked':
            raise ValueError(f'{entry["id"]} is blocked for {platform}: {policy.get("reason", "unsupported runtime")}')
        if mode not in ('full', 'instructions'):
            raise ValueError(f'Unknown delivery mode: {mode}')
        source = sets.safe_path(root, policy.get('source', entry['path']))
        target = Path(prefix) / entry['name']
        override = sets.safe_path(root, policy['override']) if policy.get('override') else None
        if mode == 'instructions' and not override:
            raise ValueError(f'Instruction-only delivery needs an override: {entry["id"]}')
        if source != sets.safe_path(root, entry['path']):
            expected = policy.get('package_sha256')
            if not expected or sets.package_hash(source) != expected:
                raise ValueError(f'Unverified provider variant: {entry["id"]}')
        if override:
            verified_artifact(root, policy['override'], artifacts)
        files = sorted(source.rglob('*'))
        for path in files:
            if path.is_symlink():
                raise ValueError(f'Symlink in provider package: {path}')
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            if mode == 'instructions' and not re.match(r'^(LICENSE|NOTICE|COPYING)(\.|$)', path.name, re.I):
                continue
            dest = target / relative
            if dest.as_posix() in payload:
                raise ValueError(f'Duplicate export path: {dest}')
            payload[dest.as_posix()] = path.read_bytes()
            source_map[path.resolve()] = dest
        main = target / 'SKILL.md'
        text = (override if mode == 'instructions' else source / 'SKILL.md').read_text(encoding='utf-8')
        prepend = override.read_text(encoding='utf-8') if override and mode == 'full' else ''
        payload[main.as_posix()] = with_policy(text, entry['name'], mode == 'instructions', prepend).encode()
        if mode == 'full':
            source_map[(source / 'SKILL.md').resolve()] = main
        selected.append({'id':entry['id'], 'source_sha256':entry['package_sha256'], 'mode':mode})
    related_urls = {}
    by_id = {entry['id']:entry for entry in manifest['skills']}
    for entry in entries:
        for related in entry.get('related_skills', []):
            other = by_id[related]
            provenance = other['provenance']
            if all(provenance.get(k) for k in ('repository','revision','path')):
                related_urls[sets.safe_path(root,other['path']).resolve() / 'SKILL.md'] = f'{provenance["repository"]}/blob/{provenance["revision"]}/{provenance["path"]}/SKILL.md'
    for source, dest in source_map.items():
        if dest.suffix.lower() == '.md':
            payload[dest.as_posix()] = rewrite_links(payload[dest.as_posix()].decode('utf-8'), source, source_map, related_urls).encode()
    artifact_map: dict[Path, Path] = {}

    def add_artifact(path: str) -> None:
        source = sets.safe_path(root, path).resolve()
        if source in artifact_map:
            return
        data = verified_artifact(root, path, artifacts)
        dest = Path('references/library') / path
        artifact_map[source] = dest
        payload[dest.as_posix()] = data
        record = artifacts[path]
        dependencies = list(record.get('dependencies', []))
        if record.get('license_path'):
            dependencies.append(record['license_path'])
        if source.suffix.lower() == '.md':
            for target_ in sets.markdown_links(data.decode('utf-8')):
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target_) or target_.startswith('#'):
                    continue
                linked = sets.reference_path(root, source, target_.split('#', 1)[0])
                dependencies.append(linked.relative_to(root.resolve()).as_posix())
        for dependency in dependencies:
            add_artifact(dependency)

    rendered_artifacts: list[tuple[Path, Path]] = []
    for item in bundle.get('agents', []):
        if platform not in item.get('platforms', PLATFORMS):
            continue
        path = item['path']
        add_artifact(path)
        raw = verified_artifact(root, path, artifacts).decode('utf-8')
        body = re.sub(r'^---\n.*?\n---\n?', '', raw, count=1, flags=re.S)
        name = item['name']
        if not sets.SLUG.fullmatch(name):
            raise ValueError('Unsafe agent name')
        if platform == 'copilot':
            tool_list = item.get('tools', ['read','search'])
            if not set(tool_list) <= {'read','search','edit','execute','agent'}:
                raise ValueError('Unapproved Copilot tool name')
            front = f'---\nname: {name}\ndescription: {json.dumps(item["description"])}\ntools: {json.dumps(tool_list)}\n---\n\n'
            dest = f'.github/agents/{name}.agent.md'
            body = front + POLICY + '\n' + body
        else:
            dest = f'references/agents/{name}.md'
            body = POLICY + '\n' + body
        if dest in payload:
            raise ValueError('Duplicate agent export')
        payload[dest] = body.encode()
        rendered_artifacts.append((sets.safe_path(root,path).resolve(),Path(dest)))
    for item in bundle.get('prompts', []):
        path = item['path']
        add_artifact(path)
        body = verified_artifact(root, path, artifacts).decode('utf-8')
        name = item['name']
        if not sets.SLUG.fullmatch(name):
            raise ValueError('Unsafe prompt name')
        body = re.sub(r'^---\n.*?\n---\n?', '', body, count=1, flags=re.S)
        dest = f'.github/prompts/{name}.prompt.md' if platform == 'copilot' else f'references/prompts/{name}.md'
        if dest in payload:
            raise ValueError('Duplicate prompt export')
        payload[dest] = (POLICY + '\n' + body).encode()
        rendered_artifacts.append((sets.safe_path(root,path).resolve(),Path(dest)))
    for source, dest in artifact_map.items():
        if dest.suffix.lower() == '.md':
            payload[dest.as_posix()] = rewrite_links(payload[dest.as_posix()].decode('utf-8'), source, artifact_map).encode()
    for source, dest in rendered_artifacts:
        mapping = dict(artifact_map)
        mapping[source] = dest
        payload[dest.as_posix()] = rewrite_links(payload[dest.as_posix()].decode('utf-8'), source, mapping).encode()
    # Validate every emitted Markdown link, including instruction overrides.
    for name, data in payload.items():
        if not name.endswith('.md'):
            continue
        for target_ in sets.markdown_links(data.decode('utf-8')):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target_) or target_.startswith('#'):
                continue
            resolved = os.path.normpath(str(Path(name).parent / target_.split('#', 1)[0]))
            if resolved not in payload:
                raise ValueError(f'Unresolved exported link in {name}: {target_}')
    if platform == 'chatgpt':
        plugin = {'name':'my-ai-skills-' + profile, 'version':'1.0.0', 'description':bundle['description'], 'author':{'name':'Aaron DeYoung'}, 'repository':'https://github.com/GRsoldier7/My_AI_Skills', 'extensions':{'com.openai':{'interface':{'displayName':bundle['title'], 'shortDescription':bundle['description'][:80], 'longDescription':bundle['description'], 'developerName':'Aaron DeYoung', 'category':'Productivity', 'defaultPrompt':[bundle['prompt']]}}}}
        payload['plugin.json'] = (json.dumps(plugin,indent=2)+'\n').encode()
    payload['README.md'] = (f'# {bundle["title"]}\n\nTarget: {platform}. Staged export only; no account or device installation.\n\n{bundle["description"]}\n\n{POLICY}\nNative-host discovery and behavior require separate verification.\n').encode()
    receipt = {'schema_version':1,'profile':profile,'platform':platform,'skills':selected,'files':{p:sha(v) for p,v in sorted(payload.items())}}
    payload['SOURCES.json'] = (json.dumps(receipt,indent=2)+'\n').encode()
    output = output.absolute()
    archive = output.with_suffix('.zip')
    ensure_output(output,root)
    ensure_output(archive,root)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.library-export-',dir=output.parent) as stage:
        stage_path = Path(stage)
        folder = stage_path / 'bundle'
        folder.mkdir()
        for name,data in sorted(payload.items()):
            path = folder / name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
        zip_path = stage_path / 'bundle.zip'
        with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED) as z:
            for name,data in sorted(payload.items()):
                info = zipfile.ZipInfo(name,date_time=(2026,10,29,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info,data)
        if output.exists() or archive.exists():
            raise ValueError('Output appeared during export; refusing overwrite')
        folder.rename(output)
        zip_path.rename(archive)
    return {'profile':profile,'platform':platform,'skills':len(entries),'files':len(payload),'output':str(output),'archive':str(archive)}


def catalog(root: Path, write: bool = False) -> str:
    manifest, config, artifacts = load(root)
    path = sets.safe_path(root,config['catalog_path'])
    lines = ['# ' + path.stem,'','Generated from the curated skill manifest, artifact inventory and delivery configuration. One source per package; domain profiles select capabilities. Trial status does not establish native-host readiness.','','## Start here','','| Bundle | Platforms | Purpose |','|---|---|---|']
    for name,bundle in sorted(config['bundles'].items()):
        lines.append(f'| {name} | {", ".join(bundle["platforms"])} | {bundle["description"]} |')
    categories = sorted({e['path'].split('/')[1] for e in manifest['skills']})
    for category in categories:
        lines.extend(['',f'## {category.replace("-"," ").title()}','','| Skill | Status | Domains | Runtime / platform notes | Source |','|---|---|---|---|---|'])
        for entry in sorted((e for e in manifest['skills'] if e['path'].split('/')[1] == category),key=lambda e:e['id']):
            source = entry['provenance'].get('repository','Owner-authored / historical source')
            revision = entry['provenance'].get('revision','')
            source = f'[{source.split("/")[-1]}]({source}/tree/{revision})' if source.startswith('https://') and revision else source
            runtime = entry.get('runtime','See package and platform guide')
            if not isinstance(runtime,str): runtime = json.dumps(runtime,ensure_ascii=False)
            domains = ', '.join(entry.get('domains',[])) or 'Selected profiles'
            lines.append(f'| [{entry["name"]}](../{entry["path"]}/SKILL.md) | {entry["status"]} | {domains} | {runtime.replace(chr(124),"/")} | {source} |')
    lines.extend(['','## Agents, prompts and tooling','','Canonical personas are organized by collection/division. Platform exports select roles rather than loading every persona.','','| Artifact | Type | Status / target |','|---|---|---|'])
    for path_,a in sorted(artifacts.items()):
        lines.append(f'| [{path_}](../{path_}) | {a["type"]} | {a.get("status","reference")}: {a.get("target","").replace(chr(124),"/")} |')
    result = '\n'.join(lines)+'\n'
    if write:
        path.write_text(result,encoding='utf-8',newline='\n')
    elif not path.exists() or path.read_text(encoding='utf-8') != result:
        raise ValueError('Library catalog is stale; regenerate with catalog --write')
    return str(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='action',required=True)
    index = actions.add_parser('catalog')
    index.add_argument('--write',action='store_true')
    staging = actions.add_parser('export')
    staging.add_argument('--profile',required=True)
    staging.add_argument('--platform',required=True,choices=PLATFORMS)
    staging.add_argument('--output',required=True,type=Path)
    args = parser.parse_args()
    try:
        result = catalog(ROOT,args.write) if args.action == 'catalog' else export(ROOT,args.profile,args.platform,args.output)
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,OSError) as exc:
        parser.exit(1,f'ERROR: {exc}\n')


if __name__ == '__main__':
    main()
