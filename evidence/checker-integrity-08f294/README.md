# Evidence checker repair — October 12, 2026

The accomplishments checker could return PASS for a claim whose receipt, source-export record or log had never been checked against the bundle manifest. It also accepted nested escaping paths, repository/revision relabeling, duplicate JSON keys and receipt lists, missing logs and inconsistent log lengths.

[Coordination and acceptance](https://github.com/blackboxprogramming/accomplishments/issues/4) · [Tested implementation](https://github.com/blackboxprogramming/accomplishments/commit/e6960894fcf949d013501291b9a95e04b137ec84) · [Original checker](https://github.com/blackboxprogramming/accomplishments/blob/dc8a5373607649d7e3487bf1a9b373f984b15319/scripts/verify_evidence.py).

## Fresh result

The same 26 CLI regression methods produce **16 failures / 10 passes** against the unchanged original checker, then **26 passes / zero failures, errors or skips** against the repair. Each of those 16 original failures is an invalid fixture the old CLI accepted with exit 0 and PASS. The remaining ten cover valid behavior and previously enforced rejection rules. These are checker methods, not RoadOS runtime tests.

The checker now requires hashed membership for claims, every promoted receipt, its source-export record and every referenced log. It consumes the exact bytes already hashed instead of reading references again. It checks path containment, receipt log sizes, distinct passing receipts, nonempty evidence chains and matching source/receipt/claim revisions. Repository identity must match the source record; a claim's repository is checked when present, preserving older claims that omit that optional field. Duplicate JSON object keys are rejected, and count/exit metadata requires actual integers.

| Existing bundle | Manifest files | Passing receipts | Claims | Revalidation |
| --- | ---: | ---: | ---: | --- |
| Foundations | 63 | 12 | 20 | PASS |
| Core follow-up | 32 | 5 | 3 | PASS |
| Browser workflow | 50 | 2 | 4 | PASS |
| Projects workflow | 19 | 2 | 4 | PASS |

Both existing specialized browser and Projects checkers also exit 0: they recheck the committed screenshot/report hashes and saved backup observations. Original runtime and browser journeys were not executed again in this repair. The six static validation commands leave all 184 observed existing/source/test files byte-identical during execution.

## Explicit artifact-hash migration

The foundation manifest pins the evidence checker as a repository artifact. Upgrading that checker intentionally causes its old artifact digest to fail; accepting the new checker requires a reviewed digest update. The only change to the foundation manifest is that one artifact hash:

- Original SHA-256: `8990f28f35a203120ae8f5faf05496501c18ad98db13ae4cc9840abe29f57d4a`.
- Revalidated checker SHA-256: `ffb7320160719ef6197d84d736a9f53b3de869c680b698cc3d7d6d494cbcf19d`.

[Original manifest](https://github.com/blackboxprogramming/accomplishments/blob/dc8a5373607649d7e3487bf1a9b373f984b15319/evidence/2026-10-12-foundations-92286f/manifest.json) and all original receipt/claim/log/source/screenshot/download bytes remain preserved in Git history. This update changes the current checker pin; it does not rewrite any historical runtime observation. The source commit preserves all 181 unrelated original blobs.

## Receipts and reproduction

[Failed control](baseline.json) · [Raw failed-control log](baseline.stderr.log) · [Passing regression receipt](regression.json) · [Raw passing log](repaired.stderr.log) · [Six-command revalidation receipt](bundle-revalidation.json) · [Complete command outputs](bundle-revalidation-results.json) · [Source hashes](sources/accomplishments.json) · [One scoped claim](claims.json).

From a checkout containing this change:

```bash
python3 -B -m unittest discover -s tests -p 'test_verify_evidence.py' -v
python3 -B scripts/verify_evidence.py evidence/checker-integrity-08f294
python3 -B scripts/verify_evidence.py evidence/2026-10-12-foundations-92286f
python3 -B scripts/verify_evidence.py evidence/2026-10-12-core-followup-92286f
python3 -B scripts/verify_browser_evidence.py evidence/2026-10-12-browser-workflow-92286f
python3 -B scripts/verify_projects_evidence.py evidence/2026-10-12-projects-workflow-92286f
```

To reproduce the red control, point `EVIDENCE_CHECKER` at the original checker from `dc8a5373607649d7e3487bf1a9b373f984b15319` while running these new tests. It exits 1 with the 16 recorded failures.

Linux/Python 3.12.14 evidence only. Paths are checked in a static checkout; hostile concurrent filesystem mutation is not certified. A person who can rewrite both evidence and its manifest can create a self-consistent forgery. These checks establish integrity against the supplied hashes and internal consistency; they supply no signature, independent certification, semantic proof of every claim, or new test-runtime accomplishment. Review remains pending. No hosted Actions, production source, credentials, providers or deployments were changed.
