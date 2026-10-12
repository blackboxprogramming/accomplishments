# Complete RoadOS core verification — October 11, 2026 CT

The broad-core qualification gap recorded in [accomplishments #1](https://github.com/blackboxprogramming/accomplishments/issues/1) is resolved for the two pinned sources below. Both complete tracked JavaScript core test sets finished on their declared Node 26 runtime, with zero failures, cancellations or skips. No production source or test assertions were changed.

## Fresh results

| Source pin | Runtime | Result | Receipt |
| --- | --- | --- | --- |
| Original [c8c436c914314af1a3d4e5fdfd2177a371542749](https://github.com/blackboxprogramming/road-os/commit/c8c436c914314af1a3d4e5fdfd2177a371542749) | Node 26.11.1 | **532 passed**, exit 0 | [Original-pin full run](evidence/2026-10-12-core-followup-92286f/core-node26-original.json) |
| Newer merged [26c6a5913de61cad4556f04a96d017c7f7b112b5](https://github.com/blackboxprogramming/road-os/commit/26c6a5913de61cad4556f04a96d017c7f7b112b5) | Node 26.11.1 | **539 passed**, exit 0 | [Newer-pin full run](evidence/2026-10-12-core-followup-92286f/core-node26-current.json) |
| Same newer pin and complete dependency set | Node 24.19.0 | **539 passed**, exit 0 | [Same-runtime causal check](evidence/2026-10-12-core-followup-92286f/core-node24-complete.json) |
| Newer pin, Wire test file with dependency restored | Node 24.19.0 | **5 passed**, exit 0 | [Focused Wire checks](evidence/2026-10-12-core-followup-92286f/wire-complete-dependency.json) |

These runs overlap and must not be added. The seven effects-extension tests are included in the newer 539-test result. Node 24 is an additional observation; the supported-runtime qualification is the Node 26 result.

The command selects every tracked .test.js file under impl/core/tests/ and its unit/ directory. It does not run the whole RoadOS application/frontend test corpus, the separate mutation runner, deployment or every repository.

## What caused the earlier stall

The earlier assistant export contained the core folder but omitted the committed browser-side verifier at [impl/dist/products/wire.js](https://github.com/blackboxprogramming/road-os/blob/26c6a5913de61cad4556f04a96d017c7f7b112b5/impl/dist/products/wire.js). The Wire core tests import it. Its Git blob is identical at both source pins.

The focused missing-file run passed three Wire tests, failed the two that need the verifier, and did not exit before its 15-second recorder limit. One of those tests starts a Host process before importing that module; the failed import precedes its cleanup block. The independent module probe reports ERR_MODULE_NOT_FOUND and exits 1.

Adding only that committed file to a separate export made all five Wire tests complete successfully on the same Node 24 runtime. The full newer-pin suite then completed on Node 24 with the same commands and test limits as its incomplete-export baseline. This isolates the exported dependency set as the demonstrated cause of that reproduced stall.

The earlier 600-second failures remain preserved in the [foundation batch](evidence/2026-10-12-foundations-92286f/README.md). They are corrected qualification history, not evidence of a production runtime defect.

[Missing-file probe](evidence/2026-10-12-core-followup-92286f/dependency-probe-missing.json) · [Direct missing-module error](evidence/2026-10-12-core-followup-92286f/dependency-probe-missing.stderr.log) · [Focused timeout](evidence/2026-10-12-core-followup-92286f/wire-missing-dependency.json) · [Completed probe](evidence/2026-10-12-core-followup-92286f/dependency-probe-complete.json).

## What the broader result establishes

The complete core checks exercise signed identity and grants, denied operations, deterministic file writes, independent verification, tampering, restart, revocation, continuity, owner control, proof export, storage ownership and interruption recovery, Host boundaries, Wire and product-extension contracts. This is a tested local foundation supporting the approved GOAL/01 and GOAL/10 Computer experience.

The newer merged source adds seven tests for the effects Host extension: route/capability registration, status listing without inventing an authorization verdict, retained refusal records, invalid identifiers, refused proxy queueing, issuer-only release, and real-HTTP release/replay behavior. These tests were already in the source; this update independently executed them.

Passing core tests do not qualify the complete desktop, every product, fleet availability, real model inference, production security, macOS, hardware or operating uptime. No comparative cost, performance or novelty result is asserted.

## Provenance

All exported source bytes were matched to their pinned Git blob SHAs. The source manifests contain 212 files for the incomplete baseline, 213 for the newer complete core closure, and 238 for the original export with its verifier dependency restored. Before/after SHA-256 checks found no changes to the listed sources.

The official Node 26.11.1 Linux x64 archive was downloaded into an isolated scratch toolchain and matched its published SHA-256: 3883bfc73f9a680ca4eab04b196068aaaab1373ffa77d8fc1a4408222495b651. The binary version and binary SHA-256 are preserved in [toolchain provenance](evidence/2026-10-12-core-followup-92286f/node26-toolchain.json), alongside the [official checksum file](evidence/2026-10-12-core-followup-92286f/node26-official-checksums.txt). The system Node installation was not replaced. Tests ran locally on Linux; no hosted Actions or cloud inference were started.

The raw stdout/stderr, exact commands, exits, timestamps, runtimes and source hashes are committed. The observed durations are command records, not a speed comparison. The independent module probe is committed as [core_dependency_probe.mjs](scripts/core_dependency_probe.mjs).

## Reproduce

In a trusted RoadOS checkout at one of the stated pins, with its committed Wire browser verifier present and Node 26.11.1 selected:

```sh
node --version
node --test --test-concurrency=2 --test-timeout=60000 \
  impl/core/tests/*.test.js impl/core/tests/unit/*.test.js
```

The recorder also imposed a 240-second outer limit for those supported-runtime runs; per-test timeout flags alone did not terminate the incomplete-export worker in the earlier baseline.

From accomplishments, check the selected trusted checkout's verifier dependency and the evidence bundle:

```sh
node scripts/core_dependency_probe.mjs /absolute/path/to/trusted/road-os
python scripts/verify_evidence.py evidence/2026-10-12-core-followup-92286f
```

This GitHub update adds three qualification records and preserves the original twenty foundation records and their historical evidence. File-hash validation is an integrity check against the committed manifest, not third-party certification.

