#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def part1(trees):
    slope = (1,3)
    location = (0,0)
    ylen = len(trees)
    xlen = len(trees[0])
    count = 0
    while True:
        location = (location[0] + slope[0], location[1] + slope[1])
        if location[0] >= ylen:
            return count
        if location[1] >= xlen:
            location = (location[0],location[1] % xlen)
        count += trees[location]
def count_trees(trees,slope):
    location = (0,0)
    ylen = len(trees)
    xlen = len(trees[0])
    count = 0
    while True:
        location = (location[0] + slope[0], location[1] + slope[1])
        if location[0] >= ylen:
            return count
        if location[1] >= xlen:
            location = (location[0],location[1] % xlen)
        count += trees[location]
def part2(trees):
    return np.product([count_trees(trees, slope) for slope in [(1,1), (1,3), (1,5),(1,7),(2,1)]])

d = {'#': 1, '.': 0}
def parse(lines):
    return np.array([[d[x] for x in line] for line in lines],dtype=int)

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
    if p1 == 7:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 336:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
