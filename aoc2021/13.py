#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

def part1(origami):
    grid, instructions = origami
    for d, v in instructions:
        if d == 'y':
            top = grid[0:v,:]
            bottom = grid[v + 1:,:]
            grid = np.logical_or(top,np.flip(bottom,0))
            break # only one fold
        if d == 'x':
            left = grid[:,0:v]
            right = grid[:,v + 1:]
            grid = np.logical_or(left,np.flip(right,1))
            break # only one fold
    return np.count_nonzero(grid)
def print_grid(grid):
    p_d = {False: ' ', True: '█'}
    for l in grid:
        print(''.join([p_d[g] for g in l]))
def part2(origami):
    grid, instructions = origami
    for d, v in instructions:
        if d == 'y':
            top = grid[0:v,:]
            bottom = grid[v + 1:,:]
            grid = np.logical_or(top,np.flip(bottom,0))
        if d == 'x':
            left = grid[:,0:v]
            right = grid[:,v + 1:]
            grid = np.logical_or(left,np.flip(right,1))
    print_grid(grid)
    return True

def parse(lines):
    points = [p.split(',') for p in lines if len(p)>0 and  p[0].isnumeric()]
    instructions = [(l.split('=')[0][-1], int(l.split('=')[1])) for l in lines if l.find('=') != -1]
    xs = [int(p[0]) for p in points]
    ys = [int(p[1]) for p in points]
    max_x = max(xs)
    max_y = max(ys)
    grid = np.zeros((max_y + 1, max_x + 1), dtype=bool)
    for y, x in zip(ys,xs):
        grid[y][x] = True
    return (grid,instructions)
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
if p1 == 17:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == True:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
