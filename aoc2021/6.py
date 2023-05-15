#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

def calc(fish,days):
    # bincount gives the number of fish by age starting from 0
    # we need to have 0 through 8 (for the new fish)
    fish = fish + [0] * (9 - len(fish))
    for d in range(days):
        new_fish = [0] * 9
        for i in reversed(range(9)):
            if i == 0:
                new_fish[8] += fish[i]
                new_fish[6] += fish[i]
                continue
            new_fish[i - 1] += fish[i]
        fish = new_fish
    return sum(fish)
def part1(fish):
    return calc(fish,80)
def part2(fish):
    return calc(fish,256)

def parse(lines):
    fish = [ int(x) for line in lines for x in line.split(',') ]
    fish_by_age = list(np.bincount(np.array(fish,dtype=int)))
    return fish_by_age

test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(parse(test_lines))
if p1 == 5934:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(parse(lines)))
else:
    print(f"failed - {p1}")
p2 = part2(parse(test_lines))
if p2 == 26984457539:
    print("Part 2")
    print("======")
    print(p2)
    print(part2(parse(lines)))
else:
    print(f"failed - {p2}")
