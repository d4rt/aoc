#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

def part1(crabs):
    costs = [sum([abs(i-p) * c for i, c in enumerate(crabs)]) for p in range(len(crabs)) ]
    return min(costs)

def sum_n(n):
    return (n * (n + 1)) // 2

def part2(crabs):
    costs = [sum([sum_n(abs(i-p)) * c for i, c in enumerate(crabs)]) for p in range(len(crabs)) ]
    return min(costs)

def parse(lines):
    crabs = [ int(x) for line in lines for x in line.split(',') ]
    crabs_by_row = list(np.bincount(np.array(crabs,dtype=int)))
    return crabs_by_row
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
if p1 == 37:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 168:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
