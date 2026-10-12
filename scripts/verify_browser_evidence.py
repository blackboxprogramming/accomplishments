#!/usr/bin/env python3
"""Check browser report, screenshot, source and qualification consistency.

Read-only artifact consistency, not a test rerun or third-party certification.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from verify_evidence import verify_bundle


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    verified = verify_bundle(bundle)
    expected_modules = {'workspace/tests/' + name + '-browser.cjs' for name in ('startup-navigation', 'startup-input', 'document-lifecycle', 'local-computers')}
    snapshots = [('browser-workflow', 'captures', 'runner-initial.cjs', False),
                 ('browser-workflow-diagnostic', 'diagnostic-captures', 'runner-diagnostic.cjs', False),
                 ('browser-workflow-qualified', 'qualified-captures', 'runner-qualified-first.cjs', True),
                 ('browser-workflow-final', 'final-captures', None, True)]
    images = 0
    for name, folder, runner, qualified in snapshots:
        receipt = verified.read_json(name + '.json')
        report = verified.read_json(folder + '/browser-report.json')
        require(report['source_commit'] == receipt['source_commit'], 'browser revision mismatch')
        require(len(report['modules']) == len(expected_modules)
                and {item['module'] for item in report['modules']} == expected_modules, 'unexpected upstream module set')
        require(all(item['status'] == 'PASS' for item in report['modules']), 'upstream module did not pass')
        source = verified.read_json(receipt['source_export_manifest'])
        require(expected_modules <= source['files'].keys(), 'upstream source hashes missing')
        require(not report['production_source_modified'] and not report['upstream_assertions_modified'], 'modified implementation or assertions')
        require(not report['blocked_network_requests'], 'unexpected external browser request')
        require(report['http_requests'] and all(r['status'] == 200 for r in report['http_requests']), 'failed local resource request')
        require(any(r['path'] == 'desktop/assets/forest-road.jpeg' for r in report['http_requests']), 'wallpaper was not requested')
        for image, record in report['screenshots'].items():
            relative = Path(image)
            require(relative.name == image and image.endswith('-preview.jpg'), 'unsafe screenshot name')
            data = verified.read_bytes(folder + '/' + image)
            require(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], 'screenshot mismatch: ' + image)
            images += 1
        counts = receipt['reported_counts']['node']
        require(counts == {'tests': 7 if qualified else 5, 'pass': 7 if qualified else 4, 'fail': 0 if qualified else 1, 'cancelled': 0, 'skipped': 0, 'todo': 0}, 'wrong qualification counts')
        require(receipt['status'] == ('PASS' if qualified else 'FAIL') and receipt['exit_code'] == (0 if qualified else 1), 'incorrect failure/passing classification')
        if qualified:
            control = report['blank_fixture_control']
            require(control['page_url'] == 'about:blank' and control['message'].startswith('SecurityError:'), 'negative control missing')
            require(not report['application_javascript_errors'], 'application JavaScript exception')
            setup = report['test_setup_opaque_origin_errors']
            require(Counter(e['module'] for e in setup) == Counter({'startup-navigation-browser.cjs': 3, 'local-computers-browser.cjs': 1}), 'fixture error count changed')
            require(all(e['page_url'] == 'about:blank' and e['message'].startswith('SecurityError:') and 'localStorage' in e['message'] for e in setup), 'unexpected fixture exception')
            layout = report['layout']
            require([p['width'] for p in layout['panes']] == [704, 704], 'pane observation mismatch')
            require([(p['width'], p['height']) for p in layout['tiles']] == [(335, 214.5)] * 4, 'tile observation mismatch')
            require(layout['wallpaper'] == {'width': 1536, 'height': 1024}, 'wallpaper decode mismatch')
        if runner is None:
            digest = hashlib.sha256(verified.artifact_bytes('scripts/browser_workflow_runner.cjs')).hexdigest()
            require(report['runner_sha256'] == digest, 'published runner differs from final executed runner')
        else:
            digest = hashlib.sha256(verified.read_bytes(runner)).hexdigest()
            if 'runner_sha256' in report:
                require(report['runner_sha256'] == digest, 'executed runner differs from snapshot: ' + runner)
    print(json.dumps({'status': 'PASS', 'browser_reports_checked': len(snapshots), 'screenshot_hashes_checked': images, 'promoted_claims': 4, 'counts_are_not_additive': True}))


if __name__ == '__main__':
    main()
