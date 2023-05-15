#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def part1(numbers,preamble):
    previous = numbers[:preamble - 1]
    for ix, i in enumerate(numbers[preamble:]):
        if i in [x + y for ix, x in enumerate(previous) for iy, y in enumerate(previous) if ix !=iy]:
            previous = numbers[ix + 1:preamble + ix + 1]
        else:
            return i
def part2(numbers, preamble):
    target = part1(numbers, preamble)
    min_ix = 0
    for ix, i in enumerate(numbers[2:]):
        previous = numbers[min_ix:ix]
        previous_total = sum(previous)
        if previous_total == target:
            return min(previous) + max(previous)
        while previous_total > target:
            min_ix += 1
            previous = numbers[min_ix: ix]
            previous_total = sum(previous)
            if previous_total == target:
                return min(previous) + max(previous)

def parse(lines):
    return [int(x) for x in lines]

if __name__ == '__main__':
    test_infile = sys.argv[0][:-3] + '-test.txt'
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split('\n')]
    test_parsed  = parse(test_lines)

    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    lines = [x for x in data.split('\n')]
    parsed  = parse(lines)
    p1 = part1(test_parsed,5)
    print("Part 1")
    print("======")
    if p1 == 127:
        print(p1)
        print(part1(parsed,25))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed,5)
    print("Part 2")
    print("======")
    if p2 == 62:
        print(p2)
        print(part2(parsed,25))
    else:
        print(f"failed - {p2}")
