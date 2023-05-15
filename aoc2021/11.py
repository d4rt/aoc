#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

def part1(octopi):
    total_flashes = 0
    for step in tqdm(range(100)):
        # first the energy level increase by one
        octopi += 1
        # octopi greater than 9 'flash'
        flashes = octopi > 9
        w_flashes = np.where(flashes)
        flashed = flashes
        while len(w_flashes[0]) > 0:
            for fy, fx in zip(w_flashes[0], w_flashes[1]):
                from_y = max(0, fy - 1)
                from_x = max(0, fx - 1)
                octopi[from_y:fy + 2,from_x:fx + 2] += 1
                total_flashes += 1
            flashed = np.logical_or(flashed,flashes)
            flashes = np.logical_and(octopi > 9, np.logical_not(flashed))
            w_flashes = np.where(flashes)
        octopi[octopi > 9] = 0
    return total_flashes

def part2(octopi):
    step = 0
    all_flashed = False
    t = tqdm()
    while not all_flashed:
        step += 1
        t.update()
        # first the energy level increase by one
        octopi += 1
        # octopi greater than 9 'flash'
        flashes = octopi > 9
        w_flashes = np.where(flashes)
        flashed = flashes
        while len(w_flashes[0]) > 0:
            for fy, fx in zip(w_flashes[0], w_flashes[1]):
                from_y = max(0, fy - 1)
                from_x = max(0, fx - 1)
                octopi[from_y:fy + 2,from_x:fx + 2] += 1
            # don't flash the same octopus twice in a step
            flashed = np.logical_or(flashed,flashes)
            flashes = np.logical_and(octopi > 9, np.logical_not(flashed))
            w_flashes = np.where(flashes)
        octopi[octopi > 9] = 0
        all_flashed = np.all(octopi == 0)
    return 100 + step # part 1 already simulated 100 steps

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
if p1 == 1656:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 195:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
