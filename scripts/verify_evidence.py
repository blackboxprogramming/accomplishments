#!/usr/bin/env python3
"""Verify a committed evidence bundle against its hash manifest.

This checks file integrity and internal receipt consistency. A manifest is
not a signature, third-party certification, or a substitute for rerunning tests.
"""
import argparse
import hashlib
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    manifest = json.loads((bundle / 'manifest.json').read_text())
    repository = bundle.parents[1]
    for relative, digest in manifest.get('repository_artifacts', {}).items():
        path = Path(relative)
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe repository artifact path')
        require(hashlib.sha256((repository / path).read_bytes()).hexdigest() == digest,
                'repository artifact mismatch: ' + relative)
    for relative, record in manifest['files'].items():
        path = Path(relative)
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe evidence path')
        data = (bundle / path).read_bytes()
        require(len(data) == record['bytes'], 'size mismatch: ' + relative)
        require(hashlib.sha256(data).hexdigest() == record['sha256'], 'hash mismatch: ' + relative)
    for relative in manifest['pass_receipts']:
        receipt = json.loads((bundle / relative).read_text())
        require(receipt['status'] == 'PASS' and receipt['exit_code'] == 0, 'nonpassing receipt: ' + relative)
        require(receipt['source_integrity'] == {'before': [], 'after': []}, 'altered source: ' + relative)
        source = json.loads((bundle / receipt['source_export_manifest']).read_text())
        require(source['source_commit'] == receipt['source_commit'], 'revision mismatch: ' + relative)
        require(len(source['files']) == receipt['exported_files'], 'export-count mismatch: ' + relative)
        for name, record in receipt['logs'].items():
            data = (bundle / name).read_bytes()
            require(hashlib.sha256(data).hexdigest() == record['sha256'], 'receipt log mismatch: ' + name)
    claims = json.loads((bundle / 'claims.json').read_text())['claims']
    allowed = set(manifest['pass_receipts'])
    require(len({c['id'] for c in claims}) == len(claims), 'duplicate claim ID')
    for claim in claims:
        require(claim['status'] == 'PASS', 'unexpected promoted claim status')
        require(bool(claim['receipts']) and set(claim['receipts']) <= allowed,
                'claim is not tied to a passing receipt: ' + claim['id'])
    print(json.dumps({'status': 'PASS', 'files_checked': len(manifest['files']),
                      'passing_receipts_checked': len(allowed), 'claims_checked': len(claims)}))


if __name__ == '__main__':
    main()
