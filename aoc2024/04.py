#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
directions = [(0,1), (0,-1), (1,0),(-1,0), (1,1), (-1,-1),(1,-1),(-1,1)]
XMAS="XMAS"

def g(lines,x,y):
    if x < 0 or y < 0:
        return None
    try:
        return lines[x][y]
    except:
        return None

def ch(lines, i,j):
    return sum([d(lines,i,j,x,y) for x,y in directions])

def d(lines, i,j, x,y):
    for xi,c in enumerate(XMAS[1:]):
        ci = xi+1
        if g(lines,i+ci*x,j+ci*y) != c:
            return 0
    return 1


def part1(lines):
    sum = 0
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == XMAS[0]:
                # print(f"Checking {c} @ {i},{j}")
                sum += ch(lines, i,j)
    return sum

def ch2(lines, i,j):
    tl = g(lines, i-1,j-1)
    bl = g(lines, i+1,j-1)
    tr = g(lines, i-1,j+1)
    br = g(lines, i+1,j+1)
    if not tl and bl and tr and br:
        return 0
    if tl == 'M':
        if br != 'S':
            return 0
    elif tl == 'S':
        if br != 'M':
            return 0
    else:
        return 0
    if tr == 'M':
        if bl != 'S':
            return 0
    elif tr == 'S':
        if bl != 'M':
            return 0
    else:
        return 0
    return 1

def part2(lines):
    sum = 0
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == 'A':
                # print(f"Checking {c} @ {i},{j}")
                sum += ch2(lines, i,j)
    return sum


def parse(lines):
    return lines


if __name__ == "__main__":
    test_infile = sys.argv[0][:-3] + "-test.txt"
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split("\n")]
    test_parsed = parse(test_lines)

    infile = sys.argv[0][:-3] + "-input.txt"
    data = open(infile).read().strip()
    lines = [x for x in data.split("\n")]
    parsed = parse(lines)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 18:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 9:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
