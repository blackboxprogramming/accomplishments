# Native Projects evidence — 2026-10-12

[Report](../../PROJECTS_WORKFLOW_2026-10-12.md) · [Four accomplishment records](claims.json) · [Hash manifest](manifest.json) · [Source hashes](sources/road-os.json).

| Command receipt | Result | Logs |
| --- | --- | --- |
| [Native core/home](projects-domain.json) | PASS, 14/14 tests; no failures/skips/cancellations | [stdout](projects-domain.stdout.log) · [stderr](projects-domain.stderr.log) |
| [Real Chromium workflow](projects-browser.json) | PASS, 4/4 groups: two existing modules plus independent storage/backup and resource checks | [stdout](projects-browser.stdout.log) · [stderr](projects-browser.stderr.log) |

[Browser observations](captures/browser-report.json) include runtime identity, unchanged-source scope, download hashes and zero observed application exceptions/HTTP errors/non-local requests. [Raw committed workspace](captures/raw-committed-workspace.json) and all three actual [downloaded JSON files](captures/downloads/) remain available, alongside five screenshots.

The source is pinned to `8995eb202837e8cb876210b7e418fd537a937740`. All 92 exported source files stayed unchanged. Failure cases intentionally injected in the upstream storage module passed their refusal/rollback assertions; they are not failing command receipts. No RoadOS production or upstream-test edits were made.

This proves selected local Projects/Pipeline behavior on native browser IndexedDB. Local activity is not signed system authority, and backup export is not backup-import verification. Counts overlap in behavior and are not additive.

```sh
python scripts/verify_evidence.py evidence/2026-10-12-projects-workflow-92286f
python scripts/verify_projects_evidence.py evidence/2026-10-12-projects-workflow-92286f
```
