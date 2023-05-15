#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

def part1(parsed):
    from_x,from_y,to_x,to_y = parsed
    max_x = max(from_x + to_x)
    max_y = max(from_y + to_y)
    map = np.zeros((max_x + 1, max_y + 1))
    for f_x, f_y, t_x, t_y in zip(from_x, from_y, to_x, to_y):
        if f_x == t_x:
            min_y = min(f_y,t_y)
            max_y = max(f_y,t_y)
            map[f_x,min_y:max_y + 1] += 1
            continue
        if f_y == t_y:
            min_x = min(f_x,t_x)
            max_x = max(f_x,t_x)
            map[min_x:max_x + 1, f_y] += 1
        continue
    return np.count_nonzero(map >= 2)
def part2(parsed):
    from_x,from_y,to_x,to_y = parsed
    max_x = max(from_x + to_x)
    max_y = max(from_y + to_y)
    map = np.zeros((max_x + 1, max_y + 1))
    for f_x, f_y, t_x, t_y in zip(from_x, from_y, to_x, to_y):
        if f_x == t_x:
            min_y = min(f_y,t_y)
            max_y = max(f_y,t_y)
            map[f_x,min_y:max_y + 1] += 1
            continue
        if f_y == t_y:
            min_x = min(f_x,t_x)
            max_x = max(f_x,t_x)
            map[min_x:max_x + 1, f_y] += 1
            continue
        # diagonal
        if f_x < t_x:
            d_x = 1
        else:
            d_x = -1
        if f_y < t_y:
            d_y = 1
        else:
            d_y = -1
        c_x = f_x
        c_y = f_y
        while c_x != t_x:
            map[c_x][c_y] += 1
            c_x = c_x + d_x
            c_y = c_y + d_y
        map[c_x][c_y] += 1
    return np.count_nonzero(map >= 2)

def parse(lines):
    from_x = []
    from_y = []
    to_x = []
    to_y = []
    for line in lines:
        fr, to  = tuple(line.split(' -> '))
        fr_x, fr_y = tuple(fr.split(','))
        t_x, t_y = tuple(to.split(','))
        fr_x = int(fr_x)
        fr_y = int(fr_y)
        t_x = int(t_x)
        t_y = int(t_y)
        from_x.append(fr_x)
        from_y.append(fr_y)
        to_x.append(t_x)
        to_y.append(t_y)

    return (from_x,from_y,to_x,to_y)
test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = parse([x for x in test_data.split('\n')])

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = parse([x for x in data.split('\n')])

p1 = part1(test_lines)
if p1 == 5:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 12:
    print("Part 2")
    print("======")
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
