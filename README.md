# BlackRoad accomplishments

Founder and architect: **Alexa Louise Amundson**.

BlackRoad has working, tested foundations for a local-first computing system: a language implementation, scoped local operations, inspectable receipts, a browser workspace and reversible mathematical encodings.

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

The runner was Linux, Python 3.12.14 and Node 24.19.0. RoadOS core declares Node 26+; the selected results above are observations on Node 24. Its broad suite timed out and is **not qualified** by this update. Browser visual conformance, fleet deployment, cross-platform operation and the complete system verifier remain outside this batch.

Counts across rows, repeated runs, subsets and historical revisions must not be added. The byte-size comparison establishes a result for the stated workload; timing, monetary savings and novelty were not established. No hosted Actions were started.

## Earlier evidence

[Historical engineering evidence and source inspection](ENGINEERING_EVIDENCE_2026-10-11.md) remains preserved. Its recorded historical results are distinct from these fresh executions.

[Exact mathematical bounds and frame-size derivation](proofs/road94-exact-bounds.md) · [Reproduce the independent audit](scripts/verify_math.py) · [Verify the committed evidence files](scripts/verify_evidence.py).

