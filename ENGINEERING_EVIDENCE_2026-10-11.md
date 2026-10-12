# BlackRoad engineering accomplishments: evidence ledger

As of 2026-10-11. Evidence is GitHub commit metadata and reported local test outcomes, **not an independent rerun**. Counts across revisions overlap and must not be added. A passing test suite does not establish deployment, production safety, originality, or formal mathematical novelty.

| Area | Recorded finding | Primary commit |
| --- | --- | --- |
| RoadC | 160,639 local tests reported passing, zero failures/skips, after CR/CRLF/LF reader repair; three pre-fix regressions | [8b766552](https://github.com/blackboxprogramming/roadc/commit/8b76655212a1ace88c428a22a5b681222db727ec) |
| RoadC | 150,639 local tests passing after 50,000 lexical-boundary cases | [92bc08a2](https://github.com/blackboxprogramming/roadc/commit/92bc08a28a00a816a955b8b398f851e271874a37) |
| RoadC | 111,000 affected existing tests passing after executor consolidation | [32ec415b](https://github.com/blackboxprogramming/roadc/commit/32ec415b5ff559d2a7bda688a5842ed5bb54abb9) |
| RoadC | Executable offline quantum circuit simulation, Bell example, analytic tests | [9829c872](https://github.com/blackboxprogramming/roadc/commit/9829c87207eab3f89ea42f639f41e86600a5813e) |
| System | 92,868 Python and 10 JS checks passing on frozen Opportunity source, raw logs and source manifest retained | [16dc03ec](https://github.com/blackboxprogramming/system/commit/16dc03ec0a92e66ac97c23e6001f927853686835) |
| System | 92,788 Python and 10 JS tests after authorization reference protection, baseline failures retained | [43f1ab57](https://github.com/blackboxprogramming/system/commit/43f1ab57f7e192b438d3a289213ab300b75479a8) |
| RoadOS | 1,243 tests reported passing (55 optional skips) for local identity discovery integration; hardware/provider unqualified | [14d8820e](https://github.com/blackboxprogramming/road-os/commit/14d8820e2b638d942b212bf07c2316bd92c278be) |
| RoadOS | 443/443 complete backend tests, 21 focused checks for Files recovery evidence | [6c33a9c7](https://github.com/blackboxprogramming/road-os/commit/6c33a9c710c5ec3ddeccb744b275257152c938eb) |
| RoadOS | 608 product, 328 Host, 144 prototype checks and browser journeys reported on integrated source | [fb8b4762](https://github.com/blackboxprogramming/road-os/commit/fb8b47626ad02d081f4aaf8458cda4477899a0fc) |
| RoadOS | 102 workspace checks and native Chromium microphone-device interaction reported | [fec6f6ce](https://github.com/blackboxprogramming/road-os/commit/fec6f6ce676bcd65abe7da10df2376a38a1606b7) |
| Lock | Browser E2E, token/source/evidence checks, 66 renders reported passing | [8734a4a0](https://github.com/blackboxprogramming/lock/commit/8734a4a0751c640d6440b91e7cce6d0699c55aa2) |

## Test infrastructure gaps discovered and repaired in commit history

- Imported RoadOS subtree: 1,313 tests lost active workflow coverage because nested workflow files were inert at repository root: [4ffd531f](https://github.com/blackboxprogramming/road-os/commit/4ffd531f45a545ae320ef7fabd624569304c94fa).
- Canon: 449 tests were not triggered by matching workflow path filters: [6507cc44](https://github.com/blackboxprogramming/road-os/commit/6507cc4440d842fca778932ce326df48e832b74e).
- Universal: 11 suites / 137 tests had no matching active workflow: [0b75b2db](https://github.com/blackboxprogramming/road-os/commit/0b75b2db50005e9501757a0af3183b644857462e).
- Three merged suites were missing from the hand-maintained test runner: [537139ee](https://github.com/blackboxprogramming/road-os/commit/537139ee8a7713d34db722ca6327675ac01d53dd).
- An impossible iframe DOM assertion was repaired: [f57c25c8](https://github.com/blackboxprogramming/road-os/commit/f57c25c8dffd7c5ef0f71e41388823ef4fcb2e1e).

## Research and formalization

- Exact sectorial coefficient checker: [04f4d61f](https://github.com/blackboxprogramming/Amundson-Mathematics/commit/04f4d61f23bc10a70cab5bcbbab89134e4b3b341).
- REC1 non-P-recursiveness proof audit: [d8004b1a](https://github.com/blackboxprogramming/Amundson-Mathematics/commit/d8004b1a5f19b0238a8e9663793bdeb12470cc62).
- Endpoint Christoffel-growth theorem draft and proof: [bb214fdb](https://github.com/blackboxprogramming/Amundson-Mathematics/commit/bb214fdb949eb68ca414e9aad1577121afa59642).

## Next verification

Inspect committed raw logs, hash manifests and actual test runner coverage; check whether tests are independent, generated, skipped or duplicated; rerun exact pinned revisions before labeling independently reproduced. Keep original evidence in its source repositories; this index only links to it.

## Follow-up discovery: mockup and system coverage

- RoadOS [428-file mockup coverage binding and 101-app consolidation](https://github.com/blackboxprogramming/road-os/commit/1dc87112e5cf47e7716639c6d5a16f2355ad900b). Inventory/coverage work, **not** proof that 428 apps are functional.
- RoadOS [manifest gate for all 428 mockup HTML files](https://github.com/blackboxprogramming/road-os/commit/2b4e161cbbdc86cd2b8713dbfbba9e399546344e). Inspect test commands and logs before independent-pass labeling.
- RoadOS [per-file standalone mockup qualification documentation](https://github.com/blackboxprogramming/road-os/commit/aeb5f4bc17e30176b0eb4e587a4e3d1588057d50). Documentation is not itself a runtime test result.
- System [HTTP authority and strict JSON integration](https://github.com/blackboxprogramming/system/commit/a63b9142bf091fc23de814d68302434f0c317e96): commit reports 72,719 Python tests, 10 web tests, nine gates, and validated raw-log hashes. Historical result, not rerun here.

## Follow-up: receipts, recovery, and negative controls

- [RoadOS Files recovery](https://github.com/blackboxprogramming/road-os/commit/aadce1ae7ed1406353984fa0d70c57f69d131380): five pre-fix failures, 21 focused and 443 backend checks reported passing; refuses contradictory RECEIPTED evidence.
- [RoadOS storage identity reservations](https://github.com/blackboxprogramming/road-os/commit/9082fc8b075dd9e893209033c5734275e60d45fe): eleven pre-fix failures, 61 focused storage and 608 product checks reported passing; Host PID-namespace issue noted.
- [RoadOS receipt launch uncertainty](https://github.com/blackboxprogramming/road-os/commit/08985e5e7ae4e009450d1604644dd932d59ca800): errors in launch observation are recorded as unverified outcomes, rather than silently claimed nonexecution.
- [RoadOS partial outcomes](https://github.com/blackboxprogramming/road-os/commit/5fb879f0142b671fa21511c5ea15838f5661db6c): Chromium regression recorded missing PARTIAL receipt after an acknowledged step; fix records uncertain outcomes.
- [System service control-file integrity](https://github.com/blackboxprogramming/system/commit/45cd3061b9742191a98f0cc107806d85ddd5aef3): 1,000 new cases; 12,707 Python and 10 web tests reported passing, with three negative controls detected.
- [RoadOS CI cost controls](https://github.com/blackboxprogramming/road-os/commit/ec1d3bd849ae82ee368ff5eaa26b2d7dc8e1e530): 24 scoped workflows checked, including removed-test negative control; hosted Actions not asserted passing.

These are commit-reported verification claims; no tests were independently rerun in this ledger update.

## Further findings: privacy, offline operation, and security

- [RoadCode inspector avoids persisting raw questions and possible secrets](https://github.com/blackboxprogramming/road-os/commit/86afb2b122faf5353dd24a65332f0ab9ded9919a). Source change found; runtime outcome not independently rerun.
- [Signed RoadTrip collaboration](https://github.com/blackboxprogramming/road-os/commit/5f7fb8dfc710f2e749067f258e24f77163d0af1a): participant-scoped reads, signed posting and uncertainty-safe retries; inspect detailed test evidence before promotion.
- [Versioned offline Notes CRUD storage](https://github.com/blackboxprogramming/road-os/commit/9796042e91d185ac38c6136698b017a057633160). Implementation record, not live-device qualification.
- [PitStop standalone offline browser QA](https://github.com/blackboxprogramming/road-os/commit/b2fa2e1807b7d9592da3490a4435e13a878d21a9). Browser-workflow evidence record.
- [RoadC offline QFT](https://github.com/blackboxprogramming/roadc/commit/5685da2ca6c7444354f89477960fee2df7e78336): tests against all basis inputs for 1–4 qubits and inverse round trips recorded; this is simulation, not quantum hardware.
- [System object-read security verification](https://github.com/blackboxprogramming/system/commit/352c2ec11adc3ea775ed01ba28c2ad17e6662c5a): final 92,763 Python and 10 JS results reported with failing reproductions and logs; no deployment claimed.

Do not sum overlapping test suites. These are GitHub commit-derived statements, not independently executed tests.

## Direct inspection of committed machine-readable evidence (2026-10-11)

Unlike the earlier commit-message-only entries, the following JSON evidence files were fetched directly at pinned Git revisions. They are **recorded execution artifacts**, not an independent rerun or cryptographic audit of every referenced log.

1. **RoadC UTF-8 newline regression**: [result.json at 8b766552](https://github.com/blackboxprogramming/roadc/blob/8b76655212a1ace88c428a22a5b681222db727ec/evidence/source-files-10000-48541ab39699/result.json) specifies Python 3.12.14, pytest 9.1.1, Linux x86_64, exit 0, 160,639 collected, 160,639 unique case IDs, 160,639 passed, zero skipped/failed, 155.765 seconds. Three pre-fix regressions failed. Generated families include 34 groups, with 5,000 or 2,500 parameterized cases per group. The test count is **not** 160,639 independently designed test methods.
2. **RoadOS RECEIPTED Files recovery**: [report.json at 6c33a9c7](https://github.com/blackboxprogramming/road-os/blob/6c33a9c710c5ec3ddeccb744b275257152c938eb/docs/verification/storage-receipted-boundary-20261009/report.json) specifies Node 26.11.1, baseline 5/10 passing and 5 failing, repaired focused 21/21, complete backend 443/443, zero skips. It explicitly says independent human/agent review NOT_PERFORMED, and excludes multi-process locking, power-loss guarantee, authenticated browser adoption and hosted CI.
3. **System Opportunity updates**: [manifest.json at 16dc03ec](https://github.com/blackboxprogramming/system/blob/16dc03ec0a92e66ac97c23e6001f927853686835/docs/verification/opportunity-updates-20261009/manifest.json) binds source commit 39d0356c, source tree, 1,361-file closure, log SHA-256 and Git blob hashes, Python 3.12.14, Node 24.19.0, exit 0, 92,868 Python and 10 JavaScript checks, with 17 Opportunity, 20 projection and 26 project-task focused checks. It documents a single isolated assistant Linux execution; no owner Mac, GitHub Actions dispatch, provisioning or authenticated browser adapter.

**Evidence grade:** Directly inspected structured reports; test execution not reproduced here. Source manifests and raw logs are available for a subsequent byte/hash audit. Avoid describing self-reported 'independent' reviews as independent human certification.

## Raw-log inspection: stronger provenance (2026-10-11)

The following plaintext logs were directly fetched at pinned commits and their ending result lines inspected. **This confirms the committed log contents, not a new test execution.**

- RoadC [pytest.log](https://github.com/blackboxprogramming/roadc/blob/8b76655212a1ace88c428a22a5b681222db727ec/evidence/source-files-10000-48541ab39699/pytest.log): final line `160639 passed in 141.23s (0:02:21)`; Git blob `476fc321e83f005f54b6ac75d0ea8c9f7c17283b`. The separate result.json records command wall time 155.765s; this is not necessarily a contradiction because pytest runtime and whole-command duration differ.
- RoadOS [full.log](https://github.com/blackboxprogramming/road-os/blob/6c33a9c710c5ec3ddeccb744b275257152c938eb/docs/verification/storage-receipted-boundary-20261009/full.log): TAP 1..443, pass 443, fail 0, skipped 0, cancelled 0, duration 91233.848022 ms; Git blob `728297dab770c3dd9e39743615ebc642dbe6b0f9`.
- RoadOS [baseline.log](https://github.com/blackboxprogramming/road-os/blob/6c33a9c710c5ec3ddeccb744b275257152c938eb/docs/verification/storage-receipted-boundary-20261009/baseline.log): TAP 1..10, pass 5, fail 5, skipped 0; includes concrete AssertionError with expected 1 and actual 0; Git blob `ebb3564eaca46c5edd9ff216cc556d169e4decc3`.

**Next audit:** byte-compare SHA-256 checksums to manifest, inspect the actual test assertions, and rerun pinned source in an isolated environment. The logged 160,639 cases include generated parameterizations; they are not 160,639 hand-authored independent behaviors.

## Test-source inspection: assertions and test design

This pass inspected actual source files at the same pinned revisions as the preserved logs, beyond commit messages and summary JSON.

### RoadC real-file newline suite

[tests/test_source_files_10000.py](https://github.com/blackboxprogramming/roadc/blob/8b76655212a1ace88c428a22a5b681222db727ec/tests/test_source_files_10000.py) (Git blob `4192c0a8ad3d4d7480328396a2ea475b9ca0a906`) defines **four parameterized test functions with 2,500 cases each**, rather than 10,000 separate test functions. It writes real UTF-8 bytes to temporary files, exercises `run_file`, `parse_file`, `check_file`, and the lexer/interpreter directly. Assertions check preserved CR/CRLF/LF inside strings, diagnostic location and nonexecution on malformed input, and equivalence of mixed-line-ending block tokenization/execution. Values vary with `i`; structural patterns repeat. This is substantial generated regression coverage but not 10,000 independent semantic specifications.

### RoadOS signed receipt recovery

[impl/core/tests/storage-receipted-boundary.test.js](https://github.com/blackboxprogramming/road-os/blob/6c33a9c710c5ec3ddeccb744b275257152c938eb/impl/core/tests/storage-receipted-boundary.test.js) (Git blob `aed73913b5bcbde78a6526d83ca3a0b642749916`) defines **ten focused test cases**: five successful restart paths (enroll/update/move/duplicate/archive) and five faults (missing receipt, unsigned alteration, signed disagreement, wrong ID, duplicate receipt). Tests invoke real CLI subprocesses through fixtures, deliberately interrupt at RECEIPTED, compare authoritative file snapshots, require refusal without mutations, restore original evidence, retry, and run storage verification. The signed-disagreement/duplicate fixtures can re-sign altered records using a local device key; they test consistency and recovery, not adversarial key compromise. SQLite index bytes are intentionally excluded from snapshot comparison.

**Evidence tier:** source assertions inspected and linked to preserved logs. Neither suite was freshly executed during this inspection; no claim of deployment or universal correctness.

## Production source traced to tested behavior

The following source files were fetched at the same pinned revisions as the previously inspected tests and logs.

- RoadC [roadc.py](https://github.com/blackboxprogramming/roadc/blob/8b76655212a1ace88c428a22a5b681222db727ec/roadc.py), Git blob `3f9fd335673cddedc20ef9f82091468bee8c7570`: `check_file`, `run_file`, and `parse_file` open UTF-8 with `newline=""`, preserving original CR/CRLF/LF rather than applying universal newline translation.
- RoadC [lexer.py](https://github.com/blackboxprogramming/roadc/blob/8b76655212a1ace88c428a22a5b681222db727ec/lexer.py), Git blob `c23cc4adc27f87c9f67f82cd195b9dfae62b27df`: lexer branches explicitly handle carriage returns, CRLF pairs, blank lines, comment boundaries and indentation. Paired with the 10,000 generated real-file test cases and the 160,639-case log.
- RoadOS [recover.js](https://github.com/blackboxprogramming/road-os/blob/6c33a9c710c5ec3ddeccb744b275257152c938eb/impl/core/src/storage/recover.js), Git blob `46ff46d952d6e16fb6e7fbc5f777919a0f79e7bc`: before advancing from RECEIPTED to COMMITTED, recovery calls `writeTransitionRecord(tx, { requireExisting: receipted })`, explicitly requiring the original persisted transition record for an already-receipted transaction. Contradicted file bytes are rejected in move/duplicate rollback branches. The separate transition-record helper's internals are not fully audited by this inspection.

**Evidence grade:** exact-revision source-to-assertion trace plus preserved passing/failing logs. No independent rerun or complete security audit.
