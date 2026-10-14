# Amundson constant research — October 13, 2026

Accomplishment recorded for **Alexa Louise Amundson**, founder and architect of BlackRoad. Research direction and mathematical exploration were developed with AI-assisted derivation, implementation and literature checking.

**Led research on a proposed mathematical constant, producing two agreeing exact-arithmetic certificates for 100,000 decimal places, written coefficient theorems, reproducible verification tools and a documented prior-art audit.**

Recorded here on October 13, 2026, America/Chicago (October 14 UTC), after inspecting the pinned source and recorded verification results.

## Exact object

For positive integers $n$, define

$$
G_n=\frac{n^{n+1}}{(n+1)^n},\qquad
A_G=\sum_{n=1}^{\infty}\frac{G_n}{n!}
=1.24433178398672537413506162925844\ldots.
$$

The series is dimensionless and converges by comparison with the exponential series. “Proposed Amundson constant” is its working name in this research.

## Recorded results

| Result | Status and scope | Pinned evidence |
| --- | --- | --- |
| 100,000 fractional decimal places certified | COMPUTATIONAL: two exact integer enclosures agree on every reported digit, each retaining 25,209 terms. These are two methods certifying the same prefix, not 200,000 distinct digits. | [Precision receipt](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/precision-verification.json) · [Error-bound proof](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/proofs/amundson_constant_precision.md) |
| Positive half-shift expansion, exact positivity threshold and quarter-gap law | PROVED at written-proof level for the specified coefficient family; no proof-assistant verification claimed. | [Half-shift proof](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/proofs/amundson_half_shift_and_quarter_limit.md) |
| Rational bounds on $e$, exact floor identities and explicit error limits | PROVED at written-proof level; exact finite checks cover indices 1 through 256, with four targeted mutations rejected. Finite checks corroborate the universal written argument. | [Adjacent-pair proof](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/proofs/amundson_adjacent_pair_bounds.md) · [Verification receipt](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/adjacent-pair-originality.json) |
| Finite rational-denominator exclusion | If $A_G$ is rational in lowest terms, its denominator exceeds $10^{50003}$ according to the exact neighboring-fraction certificate. This finite result does not establish irrationality. | [Precision receipt](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/precision-verification.json) · [Arithmetic derivation](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/proofs/amundson_constant_precision.md) |
| Reproducible catalog and equation audit | COMPUTATIONAL / OPEN priority: ten specified digit and coefficient patterns were absent from 400,215 numeric OEIS records in the hash-bound snapshot. Positive controls were recovered; 470 additional name-only records remain a numeric coverage gap. Direct equation searches located prior art for ingredients but no earlier equivalent of the exact sum or specialized bounds. | [Audit](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/research/amundson-novelty-catalog-audit-20261013.md) · [Catalog receipt](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/novelty-catalog-audit.json) · [Snapshot checker](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/research/tools/audit_amundson_catalog_snapshot.py) |

These results have different scopes and are not additive test or discovery counts. The source also records probability and moment representations; they are linked through the research proofs rather than promoted here as separate discoveries.

## Source and verification index

All RoadMath links in this entry are pinned to source revision **3321d2e97332c953c0c19fb957f8fdc73927af61**. The work is recorded in [RoadMath PR #66](https://github.com/blackboxprogramming/roadmath/pull/66), which was open when this entry was prepared. The RoadMath repository remains private; its source links require repository access.

| Artifact at the source pin | Git blob |
| --- | --- |
| [Precision proof](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/proofs/amundson_constant_precision.md) | 6d3753f7dd6f1254f4c15d3545d85c9f1cd8bd7f |
| [Precision verification receipt](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/precision-verification.json) | 2f472a04beb146bd3295686f6810d37b35c22acb |
| [Executed command record](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/execution.json) | 04a9f58afbd36501957441d4e236c1ab41414125 |
| [Adjacent-pair proof](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/proofs/amundson_adjacent_pair_bounds.md) | 7b73e912fd557711c1ef136a358f5f7daf2dd257 |
| [Adjacent-pair verification receipt](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/adjacent-pair-originality.json) | c722817aa10d0376440d77ffc338aa79ee212f71 |
| [Current novelty audit](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/research/amundson-novelty-catalog-audit-20261013.md) | d26a54b7d66d06a3732da6ee186139f7254242f2 |
| [Current catalog and equation receipt](https://github.com/blackboxprogramming/roadmath/blob/3321d2e97332c953c0c19fb957f8fdc73927af61/provenance/constant-precision-20261013/novelty-catalog-audit.json) | 80438c4b2e82569be9776f8d75dffffa0b214203 |

The precision record reports successful scaled and direct 100,000-place commands and 17 primary focused tests. The coefficient receipt reports agreement between exact coefficient routes, strict-bound checks, floor checks and mutation rejections. These are already recorded executions; this accomplishments update did not rerun the 100,000-place calculation, the full snapshot scan or the full repository suite. The pinned proof and checker files give reproduction instructions for a trusted checkout.

## Novelty and interpretation

Historical novelty remains **OPEN**. The appropriate research description is **“apparently new in the sources checked; no earlier equivalent located.”** A relevant 2025 primary paper still has an unresolved full-text comparison. A no-match search is bounded evidence, not a guarantee of first publication.

The continuous power function, partial-function counting ingredients and general series transform have established prior art, which the source audit credits. The photographed polynomial $x(x^2+1)/2$ is a separate known formula and is not presented as a new discovery or as a derivation of $A_G$.

The accomplishment is the documented research program, exact-arithmetic certification, specialized written results and reproducible evidence. Accepted naming, first discovery, irrationality and transcendence are not established by this entry.
