#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def parse_pass(p):
    """
    The first 7 characters will either be `F` or `B`;
    these specify exactly one of the *128 rows* on the plane (numbered `0` through `127`).
    Each letter tells you which half of a region the given seat is in.
    Start with the whole list of rows; the first letter indicates whether the seat is in the *front* (`0` through `63`)
    or the *back* (`64` through `127`). The next letter indicates which half of that region the seat is in,
    and so on until you're left with exactly one row.

    >>> parse_pass('BFFFBBFRRR')
    (70, 7)
    >>> parse_pass('FFFBBBFRRR')
    (14, 7)
    >>> parse_pass('BBFFBBFRLL')
    (102, 4)
    """
    binary_row = '0b' + ''.join(['1' if x=='B' else '0' for x in p[0:7]])
    row = int(binary_row,2)
    binary_col = '0b' + ''.join(['0' if x=='L' else '1' for x in p[-3:]])
    col = int(binary_col,2)
    return (row,col)

def seat_id(row,col):
    """
    Every seat also has a unique *seat ID*: multiply the row by 8, then add the column. In this example, the seat has ID `44 * 8 + 5 = *357*`.
    >>> seat_id(70, 7)
    567
    >>> seat_id(14, 7)
    119
    >>> seat_id(102, 4)
    820
    """
    return (row * 8 + col)
def part1(lines):
    max_id = 0
    for p in lines:
        row, col = parse_pass(p)
        i = seat_id(row,col)
        max_id = max(max_id,i)
    return max_id

def sum_int(f,l):
    n = (l - f) + 1
    return (n * (f + l)) // 2

def part2(lines):
    seats = [parse_pass(p) for p in lines]
    ids = [seat_id(s[0],s[1]) for s in seats]
    max_id = max(ids)
    min_id = min(ids)
    s = sum_int(min_id,max_id)
    return s - sum(ids)

def parse(lines):
    return lines

if __name__ == '__main__':
    test_infile = sys.argv[0][:-3] + '-test.txt'
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split('\n')]
    test_parsed  = parse(test_lines)

    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    lines = [x for x in data.split('\n')]
    parsed  = parse(lines)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 820:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if True:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
