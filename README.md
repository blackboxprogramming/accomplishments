# BlackRoad accomplishments

Founder and architect: **Alexa Louise Amundson**.

BlackRoad has working, tested foundations for a local-first computing system: a language implementation, scoped local operations, inspectable receipts, a browser workspace and reversible mathematical encodings.

**Why at all?** This repository lets Alexa and anyone evaluating BlackRoad trace a claim to its source and observed result. It makes scattered logs and changing revisions inspectable before someone relies on a capability.

**Why now?** Recent merges and fresh execution changed what can be demonstrated. Source-pinned runs now cover complete core qualification, real Chromium continuity, and native Projects/Pipeline storage and backup behavior that backend checks alone did not establish.

**Why this?** A GitHub evidence index keeps source ownership and history in their existing repositories while linking claims to pinned revisions, raw logs and reproducible checks. Each result retains its tested scope and trade-offs.

**What next?** Read a result below, inspect its receipt, and rerun its stated checks in a trusted checkout. The evidence checker reads the committed bundle without changing runtime state.

## Capture evidence integrity — October 12, 2026

**48/48 checker regression tests passed.** The browser and Projects checkers now reject 20 additional invalid evidence fixtures accepted by the prior version, including unhashed captures and backups, duplicate JSON keys and repeated upstream modules. All five existing evidence bundles and both specialized checkers pass static revalidation.

[Repair report, failed controls and passing logs](evidence/capture-integrity-b7be2c/README.md) · [One scoped accomplishment record](evidence/capture-integrity-b7be2c/claims.json). These are checker regressions and artifact checks; historical RoadOS runtime counts retain their original scope.

## Native Projects and Pipeline — October 12, 2026

**14 native domain/home tests and 4 Chromium check groups passed.** Real Projects, linked tasks, decisions and Pipeline follow-up history survive reload. Two-window stale edits are refused; an injected failed write rolls back without partial state. Backups read committed IndexedDB, preserve unsaved drafts and reject malformed or missing saved data.

An independent nested-project check read the raw browser database and verified five linked tasks, one completion, saved notes, pin/context continuity, and exact equality with its actual downloaded backup. [Report and screenshots](PROJECTS_WORKFLOW_2026-10-12.md) · [Four new records](evidence/2026-10-12-projects-workflow-92286f/claims.json) · [Receipts and three JSON downloads](evidence/2026-10-12-projects-workflow-92286f/README.md).

Local browser work only: no live Roadie, Salesforce sync, signed system authority or backup-import qualification follows. No hosted Actions were started; source and upstream assertions stayed unchanged.

## Real browser workflow — October 12, 2026 UTC

**7/7 scoped Chromium check groups passed:** four unchanged upstream modules plus a negative control, desktop geometry and resource/network observation. Four local Computer IDs persist; separate Code/Chat drafts, pinning, reload, stale-message rejection and early-input ordering are exercised. Outer panes measured 704 pixels each, and all four tiles measured 335 × 214.5 pixels in a two-by-two forest-background grid.

[Browser report and inspected screenshots](BROWSER_WORKFLOW_2026-10-12.md) · [Four new records](evidence/2026-10-12-browser-workflow-92286f/claims.json) · [Receipts, including initial failed observer runs](evidence/2026-10-12-browser-workflow-92286f/README.md).

These are browser-local workspaces, not four deployed machines. Four blank-document test-fixture errors remain recorded and are explained by a control without RoadOS code. No production source or upstream test assertions changed; this is not full visual, security, fleet or platform certification.

## Complete core qualification — October 11, 2026 CT

- **532 original-pin core tests passed on Node 26.11.1.**
- **539 newer-pin core tests passed on Node 26.11.1**, including seven effects Host checks.
- The same newer pin also passed **539 tests on Node 24.19.0** after completing the source dependency set.

All complete runs exited 0 with zero failures, cancellations or skips. These overlapping counts are not additive. The earlier timeout was reproduced with a missing exported browser verifier; its completed dependency set passes. [Full qualification report](CORE_QUALIFICATION_2026-10-11.md) · [Three new records](evidence/2026-10-12-core-followup-92286f/claims.json) · [Receipts](evidence/2026-10-12-core-followup-92286f/README.md).

## Fresh verification — October 11, 2026 CT

These results were executed in this session against pinned GitHub source. [Full report](FRESH_VERIFICATION_2026-10-11.md) · [20 accomplishment records](evidence/2026-10-12-foundations-92286f/claims.json) · [Raw receipts and logs](evidence/2026-10-12-foundations-92286f/README.md).

| Area | Fresh result |
| --- | --- |
| Road / RoadC | **765 core tests passed**, with 1,673 separately reported subtests. Includes six native-compiler tests and 120 quantum-related tests; those subsets are already inside the 765. |
| Local system | **56 selected Python tests and 10 web tests passed** for real startup, service lifecycle, permission-gated reads, grant-store and API boundaries. |
| RoadOS workspace | **77 tests passed**, including two tests against a real local HTTP Host. |
| RoadOS core authority | **44 selected tests passed** on this runner. **15/15 specified queued-effect mutations caught**, zero survivors. |
| Road94 codecs | **10 stages passed: 64 Python methods and 8 Node tests**. |
| Road94 independent audit | **282,752 triples recovered**, all **241,536 unused 19-bit ranks rejected**, and the exact **19-bit fixed-width bound** checked. |
| Connected relation frames | **218 bytes versus 299 bytes** for the selected 100-edge chain: **81 bytes / 27.09% smaller**, with lossless recovery. |

The foundation batch ran on Linux, Python 3.12.14 and Node 24.19.0. Its initial broad-core timeout remains preserved. The follow-up above completes the source dependency set and qualifies both pinned core suites on Node 26.11.1. Browser visual conformance, fleet deployment, cross-platform operation and the complete system verifier remain outside these batches.

Counts across rows, repeated runs, subsets and historical revisions must not be added. The byte-size comparison establishes a result for the stated workload; timing, monetary savings and novelty were not established. No hosted Actions were started.

## Earlier evidence

[Historical engineering evidence and source inspection](ENGINEERING_EVIDENCE_2026-10-11.md) remains preserved. Its recorded historical results are distinct from these fresh executions.

[Exact mathematical bounds and frame-size derivation](proofs/road94-exact-bounds.md) · [Reproduce the independent audit](scripts/verify_math.py) · [Verify the committed evidence files](scripts/verify_evidence.py).

[Evidence checker repair and four-bundle revalidation](evidence/checker-integrity-08f294/README.md): 26 checker regressions pass after reproducing 16 false-PASS cases. This verifies the evidence chain; it adds no RoadOS runtime test count.
