# Capture evidence integrity follow-up — October 12, 2026

The browser and Projects evidence checkers reopened reports, screenshots and backup files after the general verifier ran. Those references could be absent from the hash manifest and still produce PASS. Ordinary JSON parsing also hid duplicate keys, and set comparison hid repeated upstream modules.

[Existing PR #5](https://github.com/blackboxprogramming/accomplishments/pull/5) · [Tested source](https://github.com/blackboxprogramming/accomplishments/commit/e2b8ec311ed644036f0ada9758061bd500deff10) · [Published baseline](https://github.com/blackboxprogramming/accomplishments/commit/1761ed4287cbc827d9fe388edc8cee08317d2c84) · [One scoped claim](claims.json).

## Fresh results

The same **22 capture CLI methods** produce **20 failures and two valid-fixture passes** against the unchanged published checkers. Every failing method supplies an invalid real-bundle fixture that the baseline accepted with exit 0 and PASS. Against the repair, these 22 methods and the 26 existing general-checker methods all pass: **48 tests, zero failures, errors or skips**. The full regression receipt and raw stderr retain the actual unittest output.

| Input boundary | Verified repair |
| --- | --- |
| Reports and failed observer receipts | Referenced bytes must be in the bundle hash manifest. |
| Screenshots, downloaded backups and raw database observations | References must be hashed and contained within the evidence directory. External symlinks are rejected. |
| Published runners and archived runner snapshots | Published runner bytes require repository-artifact membership; archived snapshots require bundle membership. |
| JSON reports, receipts, backups and embedded Project records | Duplicate object keys are rejected by the shared strict reader. |
| Upstream module observations | The exact module set and its cardinality must match, so repeated modules cannot pass. |
| Result output | The specialized CLI emits PASS only after its own full verification succeeds. |

The specialized checkers consume the bytes the general verifier already hashed. They do not reopen these files to interpret a later version. Existing general CLI output and receipt/claim requirements remain compatible.

## Existing evidence revalidation

All five existing bundles pass the repaired general verifier. Both specialized checkers also pass, producing seven successful artifact-check commands. Those seven commands leave **197 checkout files byte-identical**; the complete before/after hash maps are in [the read-only receipt](verification-readonly.json).

| Existing bundle | Manifest files | Passing receipts | Claims | Current result |
| --- | ---: | ---: | ---: | --- |
| Foundations | 63 | 12 | 20 | PASS |
| Core follow-up | 32 | 5 | 3 | PASS |
| Browser workflow | 50 | 2 | 4 | PASS |
| Projects workflow | 19 | 2 | 4 | PASS |
| Earlier checker repair | 11 | 2 | 1 | PASS |

The specialized outputs revalidate four browser reports and 28 screenshot hashes, plus five Projects screenshots and three downloaded backups. These observations retain their original runtime counts; no RoadOS suite or browser journey was executed again in this follow-up.

## Compatibility and failed intermediate checks

The first implementation incorrectly required a runner-digest field that the three early browser reports never recorded. The valid-browser fixture caught this regression; its raw [initial repair failure](capture-initial-repair.stderr.log) is retained. The corrected implementation requires each archived runner snapshot to be hashed and compares its digest when the report includes one. The final browser and Projects reports still require their recorded runner digests. The three old reports remain unchanged; no missing historical execution provenance was invented.

A later [transitive-pin failure](capture-transitive-pin.stderr.log) showed that the earlier checker-repair bundle pins the general checker and foundation manifest. Updating only the three direct checker pins left those dependent artifact hashes stale. The final revalidation uses the five explicit digest migrations below. Both failed intermediate attempts remain unpromoted diagnostic observations.

## Explicit artifact digest migrations

Only five repository-artifact digest values change across four existing manifests. Every raw claim, receipt, source-export record, log, screenshot, runner snapshot and downloaded backup from the existing bundles remains byte-identical. The source commit preserves 189 original blobs and deletes none. All prior artifact hashes and bytes remain available at the published baseline revision.

| Manifest | Artifact | Previous SHA-256 | Revalidated SHA-256 |
| --- | --- | --- | --- |
| `evidence/2026-10-12-foundations-92286f/manifest.json` | `scripts/verify_evidence.py` | `ffb7320160719ef6197d84d736a9f53b3de869c680b698cc3d7d6d494cbcf19d` | `f3828fb0bfb002cd60e38174aa79ae4a85da39a9e9b3669241b97a12a3f10d54` |
| `evidence/2026-10-12-browser-workflow-92286f/manifest.json` | `scripts/verify_browser_evidence.py` | `b0d13a8eb6935aeb4c7f2137fcdddb5e01790557b9f948d383ad9cda5909bc5b` | `cb53b1132045d2f2a597aa06cc29102413519236ea08615a1e167d133bcf9812` |
| `evidence/2026-10-12-projects-workflow-92286f/manifest.json` | `scripts/verify_projects_evidence.py` | `3c0bf32dbac816376baaa0de37a48997544d64447cac3c80ff2615a6a1dd9d01` | `cafa91ec13403dc85ddff1f2298a3c9c3c36f3953dca6bb55c0982a3f758975d` |
| `evidence/checker-integrity-08f294/manifest.json` | `scripts/verify_evidence.py` | `ffb7320160719ef6197d84d736a9f53b3de869c680b698cc3d7d6d494cbcf19d` | `f3828fb0bfb002cd60e38174aa79ae4a85da39a9e9b3669241b97a12a3f10d54` |
| `evidence/checker-integrity-08f294/manifest.json` | `evidence/2026-10-12-foundations-92286f/manifest.json` | `e0df73e5642d83e8910207d816fbefbcb2c0f4ad2d09b5fe22e10104166a2475` | `df462814d17fecf75b9a42e57556a8411e38ea50dc2c3b40700f6d0de0f5c2e0` |

[Machine-readable migrations](artifact-migrations.json) · [Nine source-file hashes](sources/accomplishments.json).

## Reproduction

From a checkout containing this update:

```bash
python3 -B -m unittest discover -s tests -v
python3 -B scripts/verify_evidence.py evidence/capture-integrity-b7be2c
python3 -B scripts/verify_evidence.py evidence/checker-integrity-08f294
python3 -B scripts/verify_evidence.py evidence/2026-10-12-foundations-92286f
python3 -B scripts/verify_evidence.py evidence/2026-10-12-core-followup-92286f
python3 -B scripts/verify_browser_evidence.py evidence/2026-10-12-browser-workflow-92286f
python3 -B scripts/verify_projects_evidence.py evidence/2026-10-12-projects-workflow-92286f
```

Reproduce the 20 false-PASS controls using the three exact published checkers retained in `controls/`:

```bash
CAPTURE_CHECKER_SCRIPTS="$PWD/evidence/capture-integrity-b7be2c/controls" \
  python3 -B -m unittest discover -s tests -p 'test_verify_capture_evidence.py' -v
```

That deliberate control exits 1 with 20 failures across 22 methods. The fixture harness intentionally recalculates repository-artifact hashes for whichever checker version is under test, ensuring each failure reaches the intended capture boundary.

[Failed-control receipt](baseline.json) · [Raw control failures](capture-baseline.stderr.log) · [Passing regression receipt](regression.json) · [Raw passing regression log](verification-regression.stderr.log) · [Seven-command revalidation receipt](revalidation.json) · [Individual command metadata and log references](verification-runs.json).

Linux/Python 3.12.14 evidence. This establishes checker behavior and integrity against supplied hashes. Independent authenticity, hostile concurrent filesystem operation and historical runner identity without a recorded digest remain outside the claim. Runtime counts from previous evidence were not added or promoted as newly executed tests. No hosted Actions were started.
