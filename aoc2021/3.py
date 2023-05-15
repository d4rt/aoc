#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

def part1(lines):
    length = len(lines)
    width = len(lines[0])
    gamma_list = [0] * width
    gamma = 0
    epsilon = 0
    for w in range(width):
        for l in lines:
            gamma_list[w] += int(l[w])
        gamma_list[w] = 1 if gamma_list[w] >= length/2 else 0
        gamma += 2 ** (width - w - 1) * gamma_list[w]
        epsilon += 2 ** (width - w - 1) * (1 - gamma_list[w])

    return gamma * epsilon

def part2(lines):
    length = len(lines)
    width = len(lines[0])
    # oxygen
    candidates = lines
    w = 0
    while len(candidates) > 1:
        bit_criteria = 0
        for l in candidates:
            bit_criteria += int(l[w])
        bit_criteria = 1 if bit_criteria >= (len(candidates) / 2) else 0
        new_candidates = []
        for l in candidates:
            if int(l[w]) == bit_criteria:
                new_candidates.append(l)
        candidates = new_candidates
        w += 1
    oxygen = new_candidates[0]
    # co2
    candidates = lines
    w = 0
    while len(candidates) > 1:
        bit_criteria = 0
        for l in candidates:
            bit_criteria += int(l[w])
        bit_criteria = 0 if bit_criteria >= (len(candidates) / 2) else 1
        new_candidates = []
        for l in candidates:
            if int(l[w]) == bit_criteria:
                new_candidates.append(l)
        candidates = new_candidates
        w += 1
    co2 = new_candidates[0]
    return int(oxygen,2) * int(co2,2)
test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 198:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 230:
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
