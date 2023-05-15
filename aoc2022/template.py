#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

def part1(lines):
    pass
def part2(lines):
    pass

test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(infile).read().strip()
test_lines = [x for x in data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 0:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print("Part 2")
    print("======")
p2 = part2(test_lines)
if p2 == 0:
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
