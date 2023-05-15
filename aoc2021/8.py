#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

def part1(lines):
    ins, outs = lines
    return sum([1 if len(w) in [2, 3, 4, 7] else 0 for ws in outs for w in ws])

seven = {0: set("abcefg"), 1: set("cf"), 2: set("acdeg"), 3: set("acdfg"), 4: set("bcdf"), 5: set("abdfg"),
         6: set("abdefg"), 7: set("acf"), 8: set("abcdefg"), 9: set("abcdfg")}
# len 2 : 1
# len 3

def solve(digits):
    mappings = {}
    #  1 (len 2), 4 (len 4), 7 (len 3), 8 (len 7)
    digits_and_length = [(set(x),len(x)) for x in digits]
    for x, l in digits_and_length:
        if l == 2:
            mappings[1] = x
        if l == 3:
            mappings[7] = x
        if l == 4:
            mappings[4] = x
        if l == 7:
            mappings[8] = x
    for d,m in mappings.items():
        digits_and_length.remove((m,len(m)))
    for x, l in digits_and_length:
        if l == 6:
            # 9, 6, 0
            # 6 - 7 - only one that yields 4 remaining
            if len(x - mappings[7]) == 4:
                mappings[6] = x
                continue
            # 9 - 4 - only one that yields 2 remaining
            if len(x - mappings[4]) == 2:
                mappings[9] = x
                continue
        if l == 5:
            # 5, 3, 2
            if len(x - mappings[7]) == 2:
                mappings[3] = x
                continue
            # 5, 3
            if len(x - mappings[4]) == 3:
                mappings[2] = x
            else:
                mappings[5] = x
            continue
    for d, m in mappings.items():
        if (m,len(m)) in digits_and_length:
            digits_and_length.remove((m,len(m)))
    mappings[0] = digits_and_length[0][0]
    # return the reverse mapping
    return {frozenset(v): k for k, v in mappings.items()}

def part2(lines):
    ins, outs = lines
    total = 0
    for i, o in zip(ins,outs):
       # crib mapping for a with difference between 1 and 7
       mappings = solve(i)
       # print(f"{[(x,mappings[frozenset(x)]) for x in o]}")
       total += sum([(10 ** (3 - i)) * mappings[frozenset(oo)] for i, oo in enumerate(o)])
    return total


def parse(lines):
    ins = []
    outs = []
    for line in lines:
        i, o = tuple(line.split(" | "))
        i = i.split(" ")
        o = o.split(" ")
        ins.append(i)
        outs.append(o)
    return (ins,outs)
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
if p1 == 26:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 61229:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
