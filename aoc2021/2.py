#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

def part1(lines):
    horizontal = 0
    depth = 0
    for ins in lines:
        dir, unit = ins.split(" ")
        unit = int(unit)
        if dir == "forward":
            horizontal += unit
        if dir == "down":
            depth += unit
        if dir == "up":
            depth -= unit
    return horizontal * depth

def part2(lines):
    horizontal = 0
    depth = 0
    aim = 0
    for ins in lines:
        dir, unit = ins.split(" ")
        unit = int(unit)
        if dir == "forward":
            horizontal += unit
            depth += aim * unit
        if dir == "down":
            aim += unit
        if dir == "up":
            aim -= unit
    return horizontal * depth
test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 150:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 900:
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
