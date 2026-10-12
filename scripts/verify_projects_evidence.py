#!/usr/bin/env python3
"""Read-only consistency check for pinned native Projects evidence."""
import argparse
import hashlib
import json
from pathlib import Path
from verify_evidence import read_json, verify_bundle


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    bundle = parser.parse_args().bundle.resolve()
    verified = verify_bundle(bundle)
    browser = verified.read_json('projects-browser.json')
    domain = verified.read_json('projects-domain.json')
    source = verified.read_json('sources/road-os.json')
    report = verified.read_json('captures/browser-report.json')
    require(browser['source_commit'] == domain['source_commit'] == source['source_commit'] == report['source_commit'], 'revision mismatch')
    require(browser['reported_counts']['node'] == {'tests': 4, 'pass': 4, 'fail': 0, 'cancelled': 0, 'skipped': 0, 'todo': 0}, 'browser group count mismatch')
    require(domain['reported_counts']['node'] == {'tests': 14, 'pass': 14, 'fail': 0, 'cancelled': 0, 'skipped': 0, 'todo': 0}, 'native domain count mismatch')
    expected = {'desktop/apps/tests/roadwork-browser.cjs', 'desktop/apps/tests/roadwork-storage-browser.cjs'}
    require(len(report['modules']) == len(expected)
            and {item['module'] for item in report['modules']} == expected, 'upstream module set mismatch')
    require(all(item['status'] == 'PASS' for item in report['modules']), 'upstream module failure')
    require(expected <= source['files'].keys(), 'source module hashes missing')
    require(not report['production_source_modified'] and not report['upstream_assertions_modified'], 'source/assertions were changed')
    require(not report['javascript_errors'] and not report['blocked_requests'], 'unexpected exception/network request')
    require(report['http_requests'] and all(r['status'] == 200 for r in report['http_requests']), 'resource error')
    require(report['runner_sha256'] == hashlib.sha256(verified.artifact_bytes('scripts/projects_workflow_runner.cjs')).hexdigest(), 'runner differs from execution')
    for name, record in report['screenshots'].items():
        require(Path(name).name == name and name.endswith('-preview.jpg'), 'unsafe screenshot name')
        data = verified.read_bytes('captures/' + name)
        require(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], 'screenshot hash mismatch')
    require(len(report['screenshots']) == 5, 'screenshot count mismatch')
    require(len(report['downloads']) == 3, 'download count mismatch')
    for item in report['downloads']:
        relative = Path(item['path'])
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe download path')
        data = verified.read_bytes('captures/' + item['path'])
        require(item['status'] == 'SAVED' and len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256'], 'download integrity mismatch')
        snapshot = read_json(data)
        require(snapshot['revision'] == item['workspace_revision'], 'download revision mismatch')
        require({'files': len(snapshot['files']), 'tasks': len(snapshot['tasks']), 'local_activity': len(snapshot['receipts'])} == item['record_counts'], 'download count metadata mismatch')
    raw = verified.read_json('captures/raw-committed-workspace.json')
    backup = verified.read_json('captures/downloads/003-workspace.json')
    require(backup == raw, 'download differs from raw committed observation')
    require((raw['revision'], len(raw['tasks']), sum(t['done'] for t in raw['tasks'])) == (4, 5, 1), 'independent task observation mismatch')
    projects = [f for f in raw['files'] if f.get('mime') == 'application/vnd.blackroad.project+json']
    require(len(projects) == 1 and projects[0]['revision'] == 3, 'project observation mismatch')
    record = read_json(projects[0]['content'])
    require(record['title'] == 'Verified native Project' and len(set(record['taskIds'])) == 5, 'project identity/task mapping mismatch')
    require(all(any(t['id'] == identity for t in raw['tasks']) for identity in record['taskIds']), 'dangling linked task')
    require('Unsaved proposal excluded from backup' not in record['context'], 'unsaved proposal leaked into backup')
    require([r['operation'] for r in raw['receipts']] == ['project-create', 'project-task-toggle', 'project-context', 'project-task-add'], 'local operation observation mismatch')
    independent = report['independent_project']
    require(all(independent[k] for k in ('reload_raw_state_equal', 'backup_equals_raw_committed_state', 'export_left_raw_state_unchanged', 'unsaved_editor_retained', 'pin_and_left_context_retained')), 'independent observation failed')
    require(independent['canonical_system_connection'] == 'disconnected', 'unexpected system authority')
    print(json.dumps({'status': 'PASS', 'browser_groups': 4, 'native_domain_tests': 14, 'screenshots_checked': 5, 'downloaded_backups_checked': 3, 'raw_committed_backup_equal': True, 'counts_are_not_additive': True}))


if __name__ == '__main__':
    main()
