#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

d = {'.': 0, '>': 1, 'v': 2 }
EMPTY = 0
RIGHT = 1
DOWN = 2
p = {v:k for k,v in d.items()}

def part1(grid):
    moved = True
    step = 0
    ylen = len(grid)
    xlen = len(grid[0])
    while moved:
        step += 1
        moved = False
        n = grid.copy()
        for y,x in zip(*np.where(grid == RIGHT)):
            nx = (x + 1) % xlen
            ny = y
            if grid[ny,nx] == EMPTY:
                n[ny,nx] = RIGHT
                n[y,x] = EMPTY
                moved = True
        grid = n
        n = grid.copy()
        for y,x in zip(*np.where(grid == DOWN)):
            nx = x
            ny = (y + 1) % ylen
            if grid[ny,nx] == EMPTY:
                n[ny,nx] = DOWN
                n[y,x] = EMPTY
                moved = True
        grid = n
    return step
def part2(lines):
    pass


def print_grid(g):
    for l in g:
        print(''.join([p[x] for x in l]))

def parse(lines):
    return np.array([[ d[x] for x in line ] for line in lines],dtype=int)

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
    if p1 == 58:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 5:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
