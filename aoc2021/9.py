#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np
import scipy
from skimage.morphology import flood_fill

def part1(tubes):
    comp_footprint = np.asarray([[0,1,0],
                                 [1,0,1],
                                 [0,1,0]])
    minima = tubes < scipy.ndimage.minimum_filter(tubes,footprint=comp_footprint, mode='constant', cval=10)

    return np.sum((tubes + 1) * minima )

def part2(tubes):
    comp_footprint = np.asarray([[0,1,0],
                                 [1,0,1],
                                 [0,1,0]])
    minima = np.where(tubes < scipy.ndimage.minimum_filter(tubes,footprint=comp_footprint, mode='constant', cval=10))
    basins = np.zeros_like(tubes)
    basins[tubes == 9] = -1 # basin barriers (9s are never part of a basin)
    basin = 1
    basin_scores = []
    for my, mx in zip(minima[0],minima[1]):
        flood_fill(basins,(my,mx),basin,connectivity=1,in_place=True)
        basin_scores.append(np.count_nonzero(basins == basin))
        basin += 1

    return np.prod(sorted(basin_scores)[-3:])
def parse(lines):
    return np.asarray([[int(x) for x in line] for line in lines], dtype=int)
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
if p1 == 15:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 1134:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
