"""CLI regressions for complete evidence chains using real files and hashes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(os.environ.get('EVIDENCE_CHECKER',
                             str(Path(__file__).resolve().parents[1] / 'scripts/verify_evidence.py')))


class EvidenceCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bundle = self.root / 'evidence' / 'example'
        self.bundle.mkdir(parents=True)
        self.source = {'source_commit': 'a' * 40, 'repository': 'owner/source',
                       'files': {'entry.py': {'sha256': 'b' * 64}}}
        self.receipt = {'status': 'PASS', 'exit_code': 0,
                        'source_integrity': {'before': [], 'after': []},
                        'repository': 'owner/source', 'source_commit': 'a' * 40,
                        'source_export_manifest': 'sources/source.json',
                        'exported_files': 1,
                        'logs': {'stdout.log': self.record(b'one test passed\n')}}
        self.claims = {'claims': [{'id': 'C1', 'status': 'PASS',
                                   'repository': 'owner/source', 'source_commit': 'a' * 40,
                                   'receipts': ['receipt.json']}]}
        self.files = {'sources/source.json': self.encode(self.source),
                      'stdout.log': b'one test passed\n',
                      'receipt.json': self.encode(self.receipt),
                      'claims.json': self.encode(self.claims)}
        self.manifest = {'files': {name: self.record(data) for name, data in self.files.items()},
                         'pass_receipts': ['receipt.json'], 'repository_artifacts': {}}
        self.save()

    @staticmethod
    def encode(value):
        return (json.dumps(value, sort_keys=True) + '\n').encode()

    @staticmethod
    def record(data):
        return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def save(self):
        for relative, data in self.files.items():
            path = self.bundle / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (self.bundle / 'manifest.json').write_bytes(self.encode(self.manifest))

    def replace_json(self, name, value):
        self.files[name] = self.encode(value)
        self.manifest['files'][name] = self.record(self.files[name])
        self.save()

    def run_checker(self):
        return subprocess.run([sys.executable, str(CHECKER), str(self.bundle)],
                              capture_output=True, text=True, timeout=10)

    def assert_rejected(self, message):
        self.save()
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('"status": "PASS"', result.stdout)
        self.assertIn(message, result.stderr)

    def test_valid_bundle_is_read_only(self):
        before = {str(p.relative_to(self.root)): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'status': 'PASS', 'files_checked': 4,
                                                    'passing_receipts_checked': 1, 'claims_checked': 1})
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes()
                                 for p in self.root.rglob('*') if p.is_file()})

    def test_claims_must_be_hashed(self):
        del self.manifest['files']['claims.json']
        self.assert_rejected('unhashed evidence reference: claims.json')

    def test_passing_receipt_must_be_hashed(self):
        del self.manifest['files']['receipt.json']
        self.assert_rejected('unhashed evidence reference: receipt.json')

    def test_source_export_must_be_hashed(self):
        del self.manifest['files']['sources/source.json']
        self.assert_rejected('unhashed evidence reference: sources/source.json')

    def test_receipt_log_must_be_hashed(self):
        del self.manifest['files']['stdout.log']
        self.assert_rejected('unhashed evidence reference: stdout.log')

    def test_nested_source_traversal_is_rejected(self):
        (self.root / 'outside.json').write_bytes(self.encode(self.source))
        self.receipt['source_export_manifest'] = '../../outside.json'
        self.replace_json('receipt.json', self.receipt)
        self.assert_rejected('unsafe evidence path')

    def test_nested_log_traversal_is_rejected(self):
        (self.root / 'outside.log').write_bytes(b'one test passed\n')
        self.receipt['logs'] = {'../../outside.log': self.record(b'one test passed\n')}
        self.replace_json('receipt.json', self.receipt)
        self.assert_rejected('unsafe evidence path')

    def test_absolute_receipt_is_rejected(self):
        self.manifest['pass_receipts'] = [str(self.bundle / 'receipt.json')]
        self.claims['claims'][0]['receipts'] = self.manifest['pass_receipts']
        self.replace_json('claims.json', self.claims)
        self.assert_rejected('unsafe evidence path')

    def test_symlink_cannot_escape_bundle(self):
        data = self.files['stdout.log']
        del self.files['stdout.log']
        (self.bundle / 'stdout.log').unlink()
        outside = self.root / 'outside.log'
        outside.write_bytes(data)
        (self.bundle / 'stdout.log').symlink_to(outside)
        self.assert_rejected('evidence path escapes root')

    def test_symlink_cannot_escape_repository_artifact_root(self):
        outside = self.root.parent / (self.root.name + '-outside')
        outside.write_bytes(b'artifact')
        self.addCleanup(outside.unlink)
        (self.root / 'artifact.txt').symlink_to(outside)
        self.manifest['repository_artifacts'] = {'artifact.txt': hashlib.sha256(b'artifact').hexdigest()}
        self.assert_rejected('repository artifact path escapes root')

    def test_log_size_metadata_must_match(self):
        self.receipt['logs']['stdout.log']['bytes'] += 1
        self.replace_json('receipt.json', self.receipt)
        self.assert_rejected('receipt log size mismatch: stdout.log')

    def test_duplicate_passing_receipts_are_rejected(self):
        self.manifest['pass_receipts'].append('receipt.json')
        self.assert_rejected('duplicate passing receipt')

    def test_empty_receipt_logs_are_rejected(self):
        self.receipt['logs'] = {}
        self.replace_json('receipt.json', self.receipt)
        self.assert_rejected('missing receipt logs')

    def test_claim_revision_must_match_receipt(self):
        self.claims['claims'][0]['source_commit'] = 'c' * 40
        self.replace_json('claims.json', self.claims)
        self.assert_rejected('claim revision mismatch: C1')

    def test_claim_repository_must_match_receipt(self):
        self.claims['claims'][0]['repository'] = 'owner/other'
        self.replace_json('claims.json', self.claims)
        self.assert_rejected('claim repository mismatch: C1')

    def test_receipt_source_repository_must_match(self):
        self.source['repository'] = 'owner/other'
        self.replace_json('sources/source.json', self.source)
        self.assert_rejected('source repository mismatch: receipt.json')

    def test_duplicate_json_keys_are_rejected(self):
        raw = self.encode(self.manifest).decode().replace('"pass_receipts": ["receipt.json"]',
                                                       '"pass_receipts": [], "pass_receipts": ["receipt.json"]')
        (self.bundle / 'manifest.json').write_text(raw)
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('duplicate JSON key: pass_receipts', result.stderr)

    def test_failed_receipt_cannot_support_claim(self):
        self.receipt['status'] = 'FAIL'
        self.replace_json('receipt.json', self.receipt)
        self.assert_rejected('nonpassing receipt: receipt.json')

    def test_duplicate_claim_ids_are_rejected(self):
        self.claims['claims'].append(dict(self.claims['claims'][0]))
        self.replace_json('claims.json', self.claims)
        self.assert_rejected('duplicate claim ID')

    def test_changed_source_is_rejected(self):
        self.receipt['source_integrity']['after'] = ['entry.py']
        self.replace_json('receipt.json', self.receipt)
        self.assert_rejected('altered source: receipt.json')

    def test_source_revision_mismatch_is_rejected(self):
        self.source['source_commit'] = 'c' * 40
        self.replace_json('sources/source.json', self.source)
        self.assert_rejected('revision mismatch: receipt.json')

    def test_source_count_mismatch_is_rejected(self):
        self.receipt['exported_files'] = 2
        self.replace_json('receipt.json', self.receipt)
        self.assert_rejected('export-count mismatch: receipt.json')

    def test_valid_empty_log_is_supported(self):
        self.files['stdout.log'] = b''
        self.receipt['logs']['stdout.log'] = self.record(b'')
        self.manifest['files']['stdout.log'] = self.record(b'')
        self.replace_json('receipt.json', self.receipt)
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_valid_repository_artifact_is_supported(self):
        (self.root / 'artifact.txt').write_bytes(b'artifact')
        self.manifest['repository_artifacts'] = {'artifact.txt': hashlib.sha256(b'artifact').hexdigest()}
        self.save()
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_tampered_hashed_file_is_rejected(self):
        self.files['stdout.log'] = b'tampered result\n'
        self.assert_rejected('mismatch: stdout.log')

    def test_unverified_claim_receipt_is_rejected(self):
        self.claims['claims'][0]['receipts'] = ['another.json']
        self.replace_json('claims.json', self.claims)
        self.assert_rejected('claim is not tied to a passing receipt: C1')


if __name__ == '__main__':
    unittest.main()
