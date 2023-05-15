#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

def part1(lines):
    ints = [ int(l) for l in lines ]
    increased = 0
    for p,c in zip(ints[:-1],ints[1:]):
        if c > p:
            increased += 1
    return increased

def part2(lines):
    ints = [ int(l) for l in lines ]
    increased = 0
    sums = [ ints[i] + ints[i + 1] + ints[i + 2] for i in range(len(ints) - 2)]
    for p,c in zip(sums[:-1],sums[1:]):
        if c > p:
            increased += 1
    return increased
test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 7:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print("Part 2")
    print("======")
p2 = part2(test_lines)
if p2 == 5:
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
