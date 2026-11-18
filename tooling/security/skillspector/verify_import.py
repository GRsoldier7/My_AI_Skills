#!/usr/bin/env python3
"""Check recorded import bytes without running scanner or candidate code."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', type=Path, help='Optional official SkillSpector Git checkout')
    args = parser.parse_args()
    manifest = json.loads((HERE / 'integration.json').read_text())
    expected_skill = set()
    for record in manifest['files']:
        path = ROOT / record['path']
        if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
            raise ValueError('Unsafe imported path: ' + record['path'])
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != record['sha256']:
            raise ValueError('Import bytes changed: ' + record['path'])
        if 'source_path' in record:
            expected_skill.add(path)
            if args.upstream:
                source = subprocess.check_output(['git', '-C', str(args.upstream), 'show',
                    manifest['official_skill']['commit'] + ':' + record['source_path']])
                if hashlib.sha256(source).hexdigest() != record['upstream_sha256']:
                    raise ValueError('Official source mismatch: ' + record['path'])
    package = ROOT / 'skills/security/skill-inspector'
    actual_skill = {p for p in package.rglob('*') if p.is_file()}
    if actual_skill != expected_skill:
        raise ValueError('Official skill file inventory changed')
    print(f"Verified {len(manifest['files'])} import files; official skill inventory and source pins retained.")
    print('Integrity verification does not approve intake or verify scanner runtime availability.')


if __name__ == '__main__':
    main()
