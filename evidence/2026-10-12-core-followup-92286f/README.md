# Complete core qualification receipts

[Report](../../CORE_QUALIFICATION_2026-10-11.md) · [Three new accomplishment records](claims.json) · [Hash manifest](manifest.json) · [Failed baseline explanations](attempts.json).

The original pinned core passed 532 tests on Node 26.11.1. The newer merged pin passed 539 on Node 26.11.1 and, separately, 539 on Node 24.19.0. Counts overlap and are not additive.

Incomplete-export failures are retained. The missing committed Wire browser verifier is independently identified, and completing that dependency set passes the focused and full checks. No production source or assertions were altered.

Run `python scripts/verify_evidence.py evidence/2026-10-12-core-followup-92286f` from accomplishments. The bundle includes exact source manifests, raw logs and official-toolchain checksum provenance. Qualification applies only to the pinned complete core test sets and observed environments.

