# Fresh execution receipts

This bundle records the October 11, 2026 CT / October 12 UTC verification batch.

[Accomplishment records](claims.json) · [Full narrative](../../FRESH_VERIFICATION_2026-10-11.md) · [Hash manifest](manifest.json) · [Failed attempts](attempts.json).

Every promoted claim points to a passing receipt with source revision, source-export file list, commands, timestamps, exit status and hashed stdout/stderr. Source lists are under sources/. Raw outputs are preserved. Counts are not additive across claims, subsets or repeated runs.

Run `python scripts/verify_evidence.py evidence/2026-10-12-foundations-92286f` from the accomplishments repository.

RoadOS core's broad run timed out on Node 24; its Node 26+ qualification remains unverified. The bounded authority, workspace and mutation results retain their explicit scopes. Hashes establish consistency with this committed bundle, not third-party certification or authenticity of a party controlling both files and manifest.

