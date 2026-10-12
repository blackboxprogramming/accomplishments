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
