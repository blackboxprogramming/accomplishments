# BlackRoad fresh verification — October 11, 2026 CT

Execution occurred on October 12 UTC. This batch turns source inspection into freshly recorded execution evidence. It adds twenty scoped accomplishment records; it does not replace the historical ledger or promote the whole platform to production readiness.

## Source and method

| Component | Pinned commit | Exported files |
| --- | --- | ---: |
| RoadC | [26db80f55c631fcb70c91c34a1c7bb603a7a4b82](https://github.com/blackboxprogramming/roadc/commit/26db80f55c631fcb70c91c34a1c7bb603a7a4b82) | 93 |
| RoadMath | [a78cc1d75abd3fda144fdaed8fe3e83a4e120e7d](https://github.com/blackboxprogramming/roadmath/commit/a78cc1d75abd3fda144fdaed8fe3e83a4e120e7d) | 20 |
| System | [16dc03ec0a92e66ac97c23e6001f927853686835](https://github.com/blackboxprogramming/system/commit/16dc03ec0a92e66ac97c23e6001f927853686835) | 381 |
| RoadOS, completed export | [c8c436c914314af1a3d4e5fdfd2177a371542749](https://github.com/blackboxprogramming/road-os/commit/c8c436c914314af1a3d4e5fdfd2177a371542749) | 237 |

Each exported UTF-8 source file was matched to its expected Git blob SHA before writing. File modes were preserved. SHA-256 checks before and after the recorded runs found no changes to those source files. The export is a declared subset of each repository, not a complete Git checkout. Source manifests list exactly which bytes were present. The mutation run used a separate copy and restored its modified source before the post-run check.

Linux, Python 3.12.14, Node 24.19.0, existing pytest and an existing C compiler were available. No dependencies were installed. Tests used temporary local records and loopback services; no live fleet or hosted inference was contacted. No hosted GitHub Actions were started.

## Fresh passing evidence

| Receipt | Result and established behavior |
| --- | --- |
| [RoadC core](evidence/2026-10-12-foundations-92286f/roadc-core.json) | 49 modules, 765 tests, zero failures; 1,673 separately reported subtests. Includes six native compiler tests and 120 quantum-related tests across seven modules. Generated batches and trusted cross-repository integration profiles were excluded. [Raw output](evidence/2026-10-12-foundations-92286f/roadc-core.stdout.log) and [JUnit](evidence/2026-10-12-foundations-92286f/roadc-core.junit.xml) preserve the counts and IDs. |
| [System startup](evidence/2026-10-12-foundations-92286f/system-start.json) | Six tests. Actual CLI/HTTP create, relationship, denial, grant, read, hash/receipt linkage, shutdown and persistent restart; static asset and port failure boundaries. |
| [System service](evidence/2026-10-12-foundations-92286f/system-service.json) | Sixteen tests. Start/status/restart/stop, concurrent lifecycle and control-file/health behavior on Linux. |
| [System object reads](evidence/2026-10-12-foundations-92286f/system-read-grant-boundaries.json) | Twenty-one tests. Denied reads do not disclose objects; references, storage, execution outcomes and evidence failures are exercised. |
| [System grants](evidence/2026-10-12-foundations-92286f/system-auth-grants.json) | Five grant-store tests. |
| [System API](evidence/2026-10-12-foundations-92286f/system-api-boundaries.json) | Eight object-security tests. |
| [System web](evidence/2026-10-12-foundations-92286f/system-web.json) | Ten Node tests for request ordering and error states. These five disjoint Python modules total 56 methods. The complete system verifier and its declaration gates were not run. |
| [RoadOS workspace](evidence/2026-10-12-foundations-92286f/roados-workspace-final.json) | Seventy-seven tests. Persistence, pin/follow, four local Computer identities, stale document/session traffic, uncertainty-safe collaboration and participant filtering. Two tests use real HTTP Host processes; other interaction tests use controlled DOM/VM collaborators. |
| [RoadOS core authority](evidence/2026-10-12-foundations-92286f/roados-core-authority.json) | Forty-four selected tests: identity, grants, denial, deterministic execution, verification, tamper rejection, restart, revocation, export, continuity, owner control, canonical records and queued effects. The nine queued-effect tests are inside this count. |
| [Queued-effect mutations](evidence/2026-10-12-foundations-92286f/roados-queued-effect-mutations.json) | 15 specified defects applied and caught, zero survivors and zero unappliable anchors. Covers stale enqueue-time decisions, ignored revocation, replay, missing request fields, signature/key-custody checks and preview side effects. [Raw mutation result](evidence/2026-10-12-foundations-92286f/roados-queued-effect-mutations.stdout.log). |
| [Road94 codecs](evidence/2026-10-12-foundations-92286f/road94-codecs.json) | Ten stages passed: 64 Python test methods and eight Node tests. Includes exact vectors, malformed frames, automatic selection, binary I/O and verifier failures. Node coverage includes 200 bidirectional mixed cases and a separate 202-input selector comparison; these are inner inputs, not extra methods. |
| [Independent Road94 audit](evidence/2026-10-12-foundations-92286f/road94-independent-final.json) | Every one of 282,752 triples recovered through rank and coordinates; 241,536 unused ranks rejected; all 32 relation matrices checked; sheet and modulo-94 counterexamples exercised. The selected connected chain used 218 bytes versus 299, and its decoded triples were compared with the input. [Exact output](evidence/2026-10-12-foundations-92286f/road94-independent-final.stdout.log). |

These are assistant-run checks using the project's existing tests and an additional independent enumeration script. They are not an independent third-party certification. Repeated runs and overlapping inputs are never added to a grand test total.

## Exact mathematical result

The defined triple domain has 94 × 32 × 94 = 282,752 elements, which exceeds 2^18 and fits in 2^19. Thus 19 bits are necessary and sufficient for a uniform fixed-width injective encoding of that complete domain.

For 100 arbitrary ordered triples, the minimum fixed-width payload is 1,811 bits. For a connected chain it is 1,163 bits, because each next starting endpoint is already specified by the preceding endpoint. Byte alignment and the same 72-byte frame overhead give 299 and 218 bytes respectively. The measured reduction is exactly 81/299, approximately 27.09%, for the stated lossless representation comparison.

[Full derivation](proofs/road94-exact-bounds.md). These are standard finite-set and modular results. No encryption, authentication, mathematical novelty, general AI result, mining result or universal compression claim follows.

## Failed attempts and qualification gaps

Failed test setup is retained rather than presented as a passing product verdict. [Attempt notes and receipts](evidence/2026-10-12-foundations-92286f/attempts.json):

- The first core directory invocation was not accepted by this runner; later checks used explicit test files.
- The first workspace export omitted the committed host client. The next export still omitted the core VERSION file. Their failure logs are preserved; adding those committed files allowed all 77 workspace tests to pass.
- An initial broad core run using the incomplete export timed out after 600 seconds.
- The completed-export broad core run also timed out after 600 seconds without a complete suite verdict. This remains an unresolved suite-completion observation in the Node 24 environment. RoadOS core declares Node >=26, so supported-runtime qualification remains unverified. Forty-four selected core tests passing does not clear this gap.
- The receipt wrapper initially misread escaped Unicode markers in the Road94 JSON log as a pytest skip count. The published codec summary is corrected from its raw stage report; the original wrapper receipt is preserved under attempts/. Test output and execution status are unchanged.

The source artifacts were not modified to obtain passing results. This batch makes no complete-core or complete-system PASS claim. macOS, Raspberry Pi, real microphones, Chromium rendering, reboot startup, device control, provider inference and cross-repository execution remain outside its scope.

## Claim dimensions

| Dimension | State for this batch |
| --- | --- |
| Capability | PASS only for the bounded behaviors attached to passing receipts. |
| Reliability | Tested negative/restart/tamper behavior passed in its stated samples. Production reliability and uptime remain NOT_MEASURED. |
| Efficiency | PASS for the deterministic 218-vs-299-byte comparison at lossless parity. General speed, CPU, memory and energy comparisons remain NOT_MEASURED. |
| Cost | NOT_MEASURED; no monetary saving is claimed. |
| Novelty | UNVERIFIED; the mathematical audit uses standard methods and asserts no novelty. |

## Reproduce

Use trusted local checkouts at the pinned commits above and the stated toolchains. The original commands, exit codes, timestamps and environment are in every receipt.

From the appropriate source repository:

```sh
python scripts/verify.py core
python scripts/verify_road94.py
node --test --test-concurrency=2 workspace/tests/*.test.mjs
python -B -m unittest discover -s tests -p test_start.py -v
python -B -m unittest discover -s tests -p test_service.py -v
python -B -m unittest discover -s tests -p test_object_read.py -v
python -B -m unittest discover -s tests -p test_auth_grants.py -v
python -B -m unittest discover -s tests -p test_api_object_security.py -v
node --test tests/test_web.js
```

The workspace and core commands belong to RoadOS; the unittest and final web commands belong to System. The selected core receipt lists all fifteen test files explicitly. To reproduce mutations, use an isolated RoadOS copy and run `node impl/core/tests/queued-effects-mutants.mjs`; it temporarily changes queue.js and restores it. Do not run that mutation command concurrently against the same source files.

From accomplishments:

```sh
python scripts/verify_math.py /absolute/path/to/trusted/roadmath
python scripts/verify_evidence.py evidence/2026-10-12-foundations-92286f
```

The evidence verifier checks committed hashes, source/receipt consistency and claim references. A self-contained hash manifest is not a signature or an authentication mechanism.

