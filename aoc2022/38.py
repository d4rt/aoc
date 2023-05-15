#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np
from itertools import cycle

EMPTY = 0
ELF = 1
m_dict = {'.': EMPTY, '#': ELF}
p_dict = {v:k for k,v in m_dict.items()}
ROW = 0
COL = 1

def trim_2d_array(arr):
    # https://stackoverflow.com/questions/55917328/numpy-trim-zeros-in-2d-or-3d
    nz = np.nonzero(arr)  # Indices of all nonzero elements
    return arr[nz[0].min():nz[0].max()+1,nz[1].min():nz[1].max()+1]

def print_map(map,trim=True):
    if trim:
        map_trimmed = trim_2d_array(map)
    else:
        map_trimmed = map
    for r in map_trimmed:
        print(''.join([p_dict[v] for v in r]))
    print()

def make_map(lines, rounds):
    # allow for up to rounds movements in each direction
    # row, col indexing
    origin = (rounds + 1, rounds + 1)
    rows = len(lines) + 2 * rounds
    cols = len(lines[0]) + 2 * rounds
    map = np.zeros((rows,cols),dtype=int)
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            map[(origin[ROW] + row, origin[COL] + col)] = m_dict[c]
    return map

def propose(elf,map,direction):
    R = elf[ROW]
    C = elf[COL]
    #mini_map = map[R-1:R+2,C-1:C+2]
    direction_check = {'N': sum(map[R-1, C-1:C+2]), 'S': sum(map[R+1, C-1:C+2]), 'W': sum(map[R-1:R+2, C-1]), 'E' : sum(map[R-1:R+2, C+1])}
    proposal = {'N': (R-1, C), 'S' : (R+1, C), 'W': (R, C-1), 'E': (R, C+1)}
    if direction_check[direction] == 0:
        return proposal[direction]

def check_adjacent(elf,map):
    R = elf[ROW]
    C = elf[COL]
    adj = np.sum(map[R-1:R+2,C-1:C+2])
    return adj != 1


def part1(lines):
    ROUNDS = 10
    map = make_map(lines,ROUNDS)
    print_map(map)
    order = cycle(['N','S','W','E'])
    for r in tqdm(range(ROUNDS)):
        elves = np.nonzero(map)
        elves = list(zip(elves[0],elves[1]))
        unmoved_elves = list(filter(lambda elf : check_adjacent(elf, map), elves)) # only consider moving if anyone is adjacent
        proposal_elves = {}
        for d in range(4):
            direction = next(order)
            for elf in unmoved_elves:
                if not elf in proposal_elves:
                    proposal = propose(elf,map,direction)
                    if proposal:
                        proposal_elves[elf] = proposal
        for elf,proposal in proposal_elves.items():
            if sum([1 if (proposal_elves[p] == proposal) else 0 for p in proposal_elves.keys()]) == 1: # is our proposal unique?
                map[elf] = EMPTY
                map[proposal] = ELF
        print_map(map)
        _ = next(order) # set up for next round
        #
    return np.count_nonzero(trim_2d_array(map)==EMPTY)

def part2(lines):
    ALLOWANCE = 100
    map = make_map(lines,ALLOWANCE)
    order = cycle(['N','S','W','E'])
    changed = True
    rounds = 0
    while changed:
        rounds += 1
        old_map = np.copy(map)
        elves = np.nonzero(map)
        elves = list(zip(elves[0],elves[1]))
        unmoved_elves = list(filter(lambda elf : check_adjacent(elf, map), elves)) # only consider moving if anyone is adjacent
        proposal_elves = {}
        for d in range(4):
            direction = next(order)
            for elf in unmoved_elves:
                if not elf in proposal_elves:
                    proposal = propose(elf,map,direction)
                    if proposal:
                        proposal_elves[elf] = proposal
        for elf,proposal in proposal_elves.items():
            if sum([1 if (proposal_elves[p] == proposal) else 0 for p in proposal_elves.keys()]) == 1: # is our proposal unique?
                map[elf] = EMPTY
                map[proposal] = ELF
        _ = next(order) # set up for next round
        changed = not np.array_equal(map,old_map)
        #
    return rounds

test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 110:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 20:
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
