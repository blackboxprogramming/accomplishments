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


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(data):
    return json.loads(data, object_pairs_hook=unique_object)


def contained_path(root, relative, label):
    require(isinstance(relative, str) and bool(relative), 'unsafe ' + label + ' path')
    path = Path(relative)
    require(not path.is_absolute() and '..' not in path.parts,
            'unsafe ' + label + ' path')
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root), label + ' path escapes root: ' + relative)
    return resolved


class VerifiedBundle:
    """Expose only bytes checked against this bundle's supplied manifests."""

    def __init__(self, root, repository, contents, artifacts):
        self.root = root
        self.repository = repository
        self._contents = contents
        self._artifacts = artifacts
        self.summary = None

    def read_bytes(self, relative):
        contained_path(self.root, relative, 'evidence')
        require(relative in self._contents, 'unhashed evidence reference: ' + relative)
        return self._contents[relative]

    def read_json(self, relative):
        return read_json(self.read_bytes(relative))

    def artifact_bytes(self, relative):
        contained_path(self.repository, relative, 'repository artifact')
        require(relative in self._artifacts, 'unhashed repository artifact reference: ' + relative)
        return self._artifacts[relative]


def verify_bundle(bundle):
    bundle = bundle.resolve()
    manifest = read_json(contained_path(bundle, 'manifest.json', 'evidence').read_bytes())
    repository = bundle.parents[1]
    artifacts = {}
    for relative, digest in manifest.get('repository_artifacts', {}).items():
        path = contained_path(repository, relative, 'repository artifact')
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest,
                'repository artifact mismatch: ' + relative)
        artifacts[relative] = data
    files = manifest['files']
    require(isinstance(files, dict) and bool(files), 'missing evidence files')
    contents = {}
    for relative, record in files.items():
        path = contained_path(bundle, relative, 'evidence')
        data = path.read_bytes()
        require(type(record['bytes']) is int and len(data) == record['bytes'],
                'size mismatch: ' + relative)
        require(hashlib.sha256(data).hexdigest() == record['sha256'], 'hash mismatch: ' + relative)
        contents[relative] = data

    verified = VerifiedBundle(bundle, repository, contents, artifacts)
    passing = manifest['pass_receipts']
    require(isinstance(passing, list) and bool(passing), 'missing passing receipts')
    receipts = {}
    for relative in passing:
        receipt = verified.read_json(relative)
        require(relative not in receipts, 'duplicate passing receipt: ' + relative)
        require(receipt['status'] == 'PASS' and type(receipt['exit_code']) is int
                and receipt['exit_code'] == 0, 'nonpassing receipt: ' + relative)
        require(receipt['source_integrity'] == {'before': [], 'after': []},
                'altered source: ' + relative)
        source = verified.read_json(receipt['source_export_manifest'])
        require(source['source_commit'] == receipt['source_commit'], 'revision mismatch: ' + relative)
        require(source['repository'] == receipt['repository'], 'source repository mismatch: ' + relative)
        require(isinstance(source['files'], dict) and bool(source['files'])
                and type(receipt['exported_files']) is int
                and len(source['files']) == receipt['exported_files'],
                'export-count mismatch: ' + relative)
        logs = receipt['logs']
        require(isinstance(logs, dict) and bool(logs), 'missing receipt logs: ' + relative)
        for name, record in logs.items():
            data = verified.read_bytes(name)
            require(type(record['bytes']) is int and len(data) == record['bytes'],
                    'receipt log size mismatch: ' + name)
            require(hashlib.sha256(data).hexdigest() == record['sha256'],
                    'receipt log mismatch: ' + name)
        receipts[relative] = receipt
    claims = verified.read_json('claims.json')['claims']
    require(isinstance(claims, list) and bool(claims), 'missing claims')
    require(len({c['id'] for c in claims}) == len(claims), 'duplicate claim ID')
    for claim in claims:
        require(claim['status'] == 'PASS', 'unexpected promoted claim status')
        require(isinstance(claim['receipts'], list) and bool(claim['receipts'])
                and set(claim['receipts']) <= receipts.keys(),
                'claim is not tied to a passing receipt: ' + claim['id'])
        for relative in claim['receipts']:
            receipt = receipts[relative]
            require(claim['source_commit'] == receipt['source_commit'],
                    'claim revision mismatch: ' + claim['id'])
            if 'repository' in claim:
                require(claim['repository'] == receipt['repository'],
                        'claim repository mismatch: ' + claim['id'])
    verified.summary = {'status': 'PASS', 'files_checked': len(files),
                        'passing_receipts_checked': len(receipts), 'claims_checked': len(claims)}
    return verified


def verify(bundle):
    return verify_bundle(bundle).summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.bundle)))


if __name__ == '__main__':
    main()
