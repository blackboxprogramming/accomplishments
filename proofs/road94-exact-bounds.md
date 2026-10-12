# Road94: exact domain bounds and measured frame sizes

Verified on 2026-10-12 UTC, with [fresh execution evidence](../evidence/2026-10-12-foundations-92286f/README.md).

## Typed triples and the 19-bit bound

A triple has endpoints x,y in {0,...,93} and one explicitly retained relation code k in {1,...,32}. The domain has

N = 94 × 32 × 94 = 282,752 elements.

A fixed-width b-bit injective encoding must provide at least N codewords. Because 2^18 = 262,144 < N ≤ 524,288 = 2^19, at least 19 bits are necessary. Enumerating the finite Cartesian product gives a rank from 0 through 282,751 and supplies a 19-bit encoding. Successive quotient/remainder operations recover the original triple.

The independent audit compared the production rank with the ordinal of that enumeration for every triple, checked both rank and coordinate recovery, and rejected every one of the 241,536 unused 19-bit ranks. The audit's cases are domain elements, not independently authored test methods.

## Why BR37 coordinates retain the sheets

For canonical endpoint representatives, write x = 37q_x + a and y = 37q_y + b. For each retained nonzero k, the residue transform is

u = a + kb (mod 37), v = a − kb (mod 37).

Its determinant −2k is nonzero in the prime field modulo 37, so it has an inverse. For residue t, let m(t) count its endpoint representatives: 3 for t ≤ 19 and 2 otherwise. Retaining R = q_x m(b) + q_y recovers both sheets by Euclidean division. The retained tuple (k,u,v,R) therefore recovers the complete original triple.

Residues alone lose information: endpoints 0 and 37 have the same residue. Direct sum/difference modulo 94 is also not injective: (0,0) and (47,47) both map to (0,0). Both counterexamples were exercised.

## A connected chain has fewer possible messages

For n arbitrary ordered triples, the capacity is (94 × 32 × 94)^n.

For a connected chain, each next x is already known from the previous y. There are 94 choices for the initial endpoint and 32 × 94 choices for each relation and next endpoint, so the capacity is 94 × (32 × 94)^n.

For either complete finite domain, the minimum uniform fixed-width payload is ceil(log2(capacity)) bits. The audit computed this exactly as (capacity − 1).bit_length(), without floating-point logarithms.

| Representation of 100 connected relations | Minimum fixed-width payload bits | Byte-aligned payload | Shared frame overhead | Complete frame |
| --- | ---: | ---: | ---: | ---: |
| General block mode | 1,811 | 227 bytes | 72 bytes | 299 bytes |
| Connected-chain mode | 1,163 | 146 bytes | 72 bytes | 218 bytes |

The measured frame reduction is 81 bytes, exactly 81/299 of the forced block frame, approximately 27.09%. Both frames carry the same selected chain and the receiver reconstructs its complete ordered triples. The comparison's baseline is the existing general block encoding of that chain.

The reduction follows from the chain's structural constraint. These are standard finite-set, mixed-radix and modular results. Optimal fixed width is relative to each stated complete domain; it does not establish optimal coding for every probability distribution or application. The format supplies no authentication or encryption, and the byte comparison establishes no timing, energy, monetary or novelty result.

Sources: [typed-relation proof](https://github.com/blackboxprogramming/roadmath/blob/a78cc1d75abd3fda144fdaed8fe3e83a4e120e7d/proofs/road94_br37_typed_relation.md), [chain proof](https://github.com/blackboxprogramming/roadmath/blob/a78cc1d75abd3fda144fdaed8fe3e83a4e120e7d/proofs/road94_relation_chain_encoding.md), and [independent audit script](../scripts/verify_math.py).

