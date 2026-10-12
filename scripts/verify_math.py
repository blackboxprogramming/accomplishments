#!/usr/bin/env python3
"""Independent enumeration and exact bounds for the published Road94 domain.

Pass an explicitly trusted, pinned roadmath checkout. This uses only the
standard library and does not install packages or connect to any service.
"""
import argparse
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('roadmath', type=Path)
    args = parser.parse_args()
    scripts = args.roadmath.resolve() / 'scripts'
    sys.path.insert(0, str(scripts))
    spec = importlib.util.spec_from_file_location('audited_relation', scripts / 'road94_br37_relation.py')
    codec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(codec)
    counter = 0
    # The oracle is the order of the Cartesian-product enumeration, rather
    # than a second implementation of the production packing formula.
    for x in range(94):
        for relation in range(1, 33):
            for y in range(94):
                triple = (x, relation, y)
                check(codec.pack(*triple) == counter, 'rank disagrees with enumeration')
                check(codec.unpack(counter) == triple, 'enumeration ordinal fails recovery')
                coordinate = codec.encode(*triple)
                check(codec.decode(*coordinate) == triple, 'coordinate recovery failed')
                counter += 1
    check(counter == 282752, 'unexpected cardinality')
    check(2**18 < counter <= 2**19, 'nineteen-bit bound failed')
    rejected = 0
    for value in range(counter, 2**19):
        try:
            codec.unpack(value)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('an unused nineteen-bit rank was accepted')
    check(rejected == 241536, 'unexpected unused-rank count')
    check(codec.encode(93, 32, 57) == (32, 30, 8, 5), 'literal coordinate anchor failed')
    for relation in range(1, 33):
        determinant = (-2 * relation) % 37
        check((determinant * pow(determinant, -1, 37)) % 37 == 1,
              'noninvertible residue transform')
    # Explicit counterexamples guard the information-loss boundary.
    check(codec.encode(0, 1, 0)[1:3] == codec.encode(37, 1, 0)[1:3],
          'expected residue-only collision missing')
    check(codec.encode(0, 1, 0)[3] != codec.encode(37, 1, 0)[3],
          'sheet information does not distinguish the collision')
    def sum_difference94(x, y):
        return ((x + y) % 94, (x - y) % 94)
    check(sum_difference94(0, 0) == sum_difference94(47, 47),
          'expected modulo-94 collision missing')
    from road94_auto_frame import encode_smallest_frame
    from road94_relation_frames import encode_frame, decode_frame
    chain = [(i % 94, i % 32 + 1, (i + 1) % 94) for i in range(100)]
    registry = bytes(32)  # Test fixture identifier; carries no semantic authority.
    selected = encode_smallest_frame(chain, registry)
    block = encode_frame(chain, 'block', registry)
    general_capacity = counter**100
    connected_capacity = 94 * (32 * 94)**100
    general_minimum_bits = (general_capacity - 1).bit_length()
    connected_minimum_bits = (connected_capacity - 1).bit_length()
    check(len(block) == 72 + (general_minimum_bits + 7) // 8,
          'general frame does not match its cardinality-derived byte width')
    check(len(selected) == 72 + (connected_minimum_bits + 7) // 8,
          'connected frame does not match its cardinality-derived byte width')
    check((len(selected), len(block)) == (218, 299), 'hundred-relation size anchor failed')
    check(decode_frame(selected, registry)['triples'] == chain, 'selected frame failed recovery')
    saving = Fraction(len(block) - len(selected), len(block))
    print(json.dumps({
        'schema': 'road94-independent-enumeration/1', 'status': 'PASS',
        'typed_triples_checked': counter,
        'rank_roundtrips_checked': counter,
        'coordinate_roundtrips_checked': counter,
        'unused_nineteen_bit_ranks_rejected': rejected,
        'minimum_uniform_fixed_width_bits': 19,
        'invertible_relation_matrices_checked': 32,
        'hundred_connected_relations': {
            'selected_frame_bytes': len(selected), 'forced_block_bytes': len(block),
            'bytes_saved': len(block) - len(selected),
            'saving_fraction': str(saving), 'saving_percent': float(100 * saving),
            'general_minimum_fixed_width_payload_bits': general_minimum_bits,
            'connected_minimum_fixed_width_payload_bits': connected_minimum_bits,
        },
        'limits': 'Standard finite-set and modular results for this domain; no novelty, encryption, AI capability or universal-compression claim.'
    }, indent=2))


if __name__ == '__main__':
    main()
