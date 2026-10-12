"""Exercise capture integrity through both CLIs and committed real bundles."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
SCRIPTS = Path(os.environ.get('CAPTURE_CHECKER_SCRIPTS', str(REPOSITORY / 'scripts')))


class CaptureFixture:
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.bundle = self.root / 'evidence' / self.bundle_name
        shutil.copytree(REPOSITORY / 'evidence' / self.bundle_name, self.bundle)
        (self.root / 'scripts').mkdir()
        for path in (REPOSITORY / 'scripts').glob('*'):
            if path.is_file():
                shutil.copyfile(path, self.root / 'scripts' / path.name)
        for name in ('verify_evidence.py', self.checker_name):
            shutil.copyfile(SCRIPTS / name, self.root / 'scripts' / name)
        self.manifest = json.loads((self.bundle / 'manifest.json').read_text())
        for name in self.manifest.get('repository_artifacts', {}):
            path = self.root / name
            if not path.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPOSITORY / name, path)
            self.manifest['repository_artifacts'][name] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.save_manifest()
        self.report = json.loads((self.bundle / self.report_name).read_text())

    @staticmethod
    def record(data):
        return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

    def save_manifest(self):
        (self.bundle / 'manifest.json').write_text(json.dumps(self.manifest) + '\n')

    def replace_bytes(self, name, data):
        (self.bundle / name).write_bytes(data)
        self.manifest['files'][name] = self.record(data)
        self.save_manifest()

    def save_report(self):
        self.replace_bytes(self.report_name, (json.dumps(self.report) + '\n').encode())

    def run_checker(self):
        return subprocess.run([sys.executable, '-B', str(self.root / 'scripts' / self.checker_name), str(self.bundle)],
                              capture_output=True, text=True, timeout=15)

    def assert_rejected(self, message):
        self.save_manifest()
        result = self.run_checker()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('"status": "PASS"', result.stdout)
        self.assertIn(message, result.stderr)

    def test_valid_bundle_remains_read_only(self):
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout.splitlines()[-1])['status'], 'PASS')
        after = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_report_must_belong_to_hash_manifest(self):
        del self.manifest['files'][self.report_name]
        self.assert_rejected('unhashed evidence reference: ' + self.report_name)

    def test_screenshot_must_belong_to_hash_manifest(self):
        name = self.capture_folder + '/' + next(iter(self.report['screenshots']))
        del self.manifest['files'][name]
        self.assert_rejected('unhashed evidence reference: ' + name)

    def test_runner_must_belong_to_artifact_manifest(self):
        del self.manifest['repository_artifacts'][self.runner_name]
        self.assert_rejected('unhashed repository artifact reference: ' + self.runner_name)

    def test_duplicate_report_key_is_rejected(self):
        data = (self.bundle / self.report_name).read_text()
        self.replace_bytes(self.report_name, ('{"source_commit": ' + json.dumps(self.report['source_commit']) + ',' + data[1:]).encode())
        self.assert_rejected('duplicate JSON key: source_commit')

    def test_duplicate_upstream_module_is_rejected(self):
        self.report['modules'].append(dict(self.report['modules'][0]))
        self.save_report()
        self.assert_rejected('module set')

    def test_unhashed_external_screenshot_symlink_is_rejected(self):
        name = self.capture_folder + '/' + next(iter(self.report['screenshots']))
        path = self.bundle / name
        outside = self.root / 'outside-preview.jpg'
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)
        del self.manifest['files'][name]
        self.assert_rejected('evidence path escapes root')


class BrowserCaptureTests(CaptureFixture, unittest.TestCase):
    bundle_name = '2026-10-12-browser-workflow-92286f'
    checker_name = 'verify_browser_evidence.py'
    report_name = 'final-captures/browser-report.json'
    capture_folder = 'final-captures'
    runner_name = 'scripts/browser_workflow_runner.cjs'

    def test_failed_observer_receipt_must_be_hashed(self):
        name = 'browser-workflow.json'
        del self.manifest['files'][name]
        self.assert_rejected('unhashed evidence reference: ' + name)

    def test_duplicate_failed_receipt_key_is_rejected(self):
        name = 'browser-workflow.json'
        data = (self.bundle / name).read_text()
        self.replace_bytes(name, ('{"exit_code": 1,' + data[1:]).encode())
        self.assert_rejected('duplicate JSON key: exit_code')

    def test_historical_runner_snapshot_must_be_hashed(self):
        name = 'runner-initial.cjs'
        del self.manifest['files'][name]
        self.assert_rejected('unhashed evidence reference: ' + name)

    def test_historical_runner_digest_is_checked_when_present(self):
        report_name = 'captures/browser-report.json'
        report = json.loads((self.bundle / report_name).read_text())
        report['runner_sha256'] = hashlib.sha256((self.bundle / 'runner-initial.cjs').read_bytes()).hexdigest()
        self.replace_bytes(report_name, (json.dumps(report) + '\n').encode())
        self.replace_bytes('runner-initial.cjs', b'// a different observer\n')
        self.assert_rejected('executed runner differs from snapshot')


class ProjectsCaptureTests(CaptureFixture, unittest.TestCase):
    bundle_name = '2026-10-12-projects-workflow-92286f'
    checker_name = 'verify_projects_evidence.py'
    report_name = 'captures/browser-report.json'
    capture_folder = 'captures'
    runner_name = 'scripts/projects_workflow_runner.cjs'

    def test_download_must_belong_to_hash_manifest(self):
        name = 'captures/downloads/003-workspace.json'
        del self.manifest['files'][name]
        self.assert_rejected('unhashed evidence reference: ' + name)

    def test_raw_database_observation_must_be_hashed(self):
        name = 'captures/raw-committed-workspace.json'
        del self.manifest['files'][name]
        self.assert_rejected('unhashed evidence reference: ' + name)

    def test_duplicate_backup_key_is_rejected(self):
        name = 'captures/downloads/003-workspace.json'
        data = (self.bundle / name).read_text()
        revision = json.loads(data)['revision']
        replacement = ('{"revision": ' + str(revision) + ',' + data[1:]).encode()
        self.replace_bytes(name, replacement)
        item = next(item for item in self.report['downloads'] if item['path'] == 'downloads/003-workspace.json')
        item.update(self.record(replacement))
        self.save_report()
        self.assert_rejected('duplicate JSON key: revision')

    def test_unhashed_external_download_symlink_is_rejected(self):
        name = 'captures/downloads/003-workspace.json'
        path = self.bundle / name
        outside = self.root / 'outside-workspace.json'
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)
        del self.manifest['files'][name]
        self.assert_rejected('evidence path escapes root')


if __name__ == '__main__':
    unittest.main()
