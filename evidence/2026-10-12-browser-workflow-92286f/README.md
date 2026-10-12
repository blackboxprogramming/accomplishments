# Browser workflow evidence — 2026-10-12 UTC

[Full report](../../BROWSER_WORKFLOW_2026-10-12.md) · [Four new records](claims.json) · [Hash manifest](manifest.json) · [Pinned source hashes](sources/road-os.json).

| Execution | Result | Observations | Runner revision |
| --- | --- | --- | --- |
| [Initial](browser-workflow.json) | FAIL, 4/5 groups; upstream four modules passed | [Report/captures](captures/) | [Initial runner](runner-initial.cjs) |
| [Diagnostic](browser-workflow-diagnostic.json) | FAIL, 4/5; four blank-page fixture errors identified | [Report/captures](diagnostic-captures/) | [Diagnostic runner](runner-diagnostic.cjs) |
| [Qualified](browser-workflow-qualified.json) | PASS, 7/7; negative control and geometry added | [Report/captures](qualified-captures/) | [Qualified runner](runner-qualified-first.cjs) |
| [Final](browser-workflow-final.json) | PASS, 7/7; final metadata and runner-hash binding | [Report/captures](final-captures/) | [Published runner](../../scripts/browser_workflow_runner.cjs) |

Each receipt records commands, UTC times, runtime, exit status, source-integrity checks and stdout/stderr hashes. The browser reports include local resource observations, fixture exceptions and screenshot hashes. Two failed executions remain explicit, not passing claims. Four fixture exceptions are still recorded in the qualified runs; the no-application-exception claim excludes only the reproduced blank-document initialization case.

Counts are not additive across modules, assertions, repeated runs, earlier bundles or accomplishment records. Layout is qualified only at 1536×1024 in this Chromium environment. No fleet, authenticated authority, agent execution, production deployment or full-platform certification follows from these results.

Verify from the repository root:

```sh
python scripts/verify_evidence.py evidence/2026-10-12-browser-workflow-92286f
python scripts/verify_browser_evidence.py evidence/2026-10-12-browser-workflow-92286f
```
