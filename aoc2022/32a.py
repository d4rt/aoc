#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

from itertools import cycle
from copy import deepcopy

infile = sys.argv[1] if len(sys.argv)>1 else (sys.argv[0][:-3] + '-test.txt')
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]
jet_dict = {'<': -1, '>' : 1}
jets = cycle([ jet_dict[x] for x in lines[0] ])

rocks = cycle([
    [[1,1,1,1]],
    [[0,1,0],
     [1,1,1],
     [0,1,0]],
    [[0,0,1],
     [0,0,1],
     [1,1,1]],
    [[1],
     [1],
     [1],
     [1]],
    [[1,1],
     [1,1]]
])
WIDTH = 7 # 1 - 7
FLOOR = 0
CAVE = [[0,0,0,0,0,0,0] , [0,0,0,0,0,0,0]  ,[0,0,0,0,0,0,0] ]

def apply_jet(jet, X, rock):
    rock_width = len(rock[0])
    print(f"{jet} {X} {rock} {rock_width}")
    X = X + jet
    if (X + rock_width) > WIDTH:
        X = X - rock_width + 1
    X = max(1,X)
    return X

def add_to_cave(rock,x,y,cave):
    # x is left, y is bottom
    # bottom is last element of rock
    for j, r in enumerate(reversed(rock)):
        rock_row = [0,0,0,0,0,0,0]
        rock_row[x:x+len(r)] = r
        cave[y-1+j] = [sum(i) for i in zip(cave[y-1+j],rock_row)]
        print(cave[y-1+j])
    return cave



def print_cave(c):
    c_d = {0:'.', 1:'#'}
    for row in reversed(range(len(c))):
        print(f"{row:05}  |" + ''+(''.join([c_d[x] for x in c[row]]) + '|'))
    print("       +-------+")


def part1():
    ROCKS = 1
    HEIGHT = 0
    while ROCKS < 2023:
        Y = HEIGHT + 4 # bottom
        X = 2# left
        falling = True
        rock = next(rocks)
        rock_width = len(rock[0])
        while (falling):
            if Y >= len(CAVE):
                CAVE.append([0,0,0,0,0,0,0])
            jet = next(jets)
            debug_cave = deepcopy(CAVE)
            debug_cave = add_to_cave(rock, X, Y, debug_cave)
            print_cave(debug_cave)
            X = apply_jet(next(jets),X,rock)
            for i in range(len(rock)):
                row = [0,0,0,0,0,0,0]
                row[X:X+rock_width] = rock[-(i + 1)]
                c = CAVE[Y-2-i]
                if sum([row[j] * c[j] for j in range(WIDTH)]) > 0:
                    falling = False
                    break
            if falling and Y > 2:
                Y = Y - 1
            else:
                for i in range(len(rock)):
                    row = [0,0,0,0,0,0,0]
                    row[X:X+rock_width] = rock[-(i + 1)]
                    HEIGHT = max(HEIGHT,Y-2-i)
                    c = CAVE[Y-2-i]
                    for j in range(WIDTH):
                        c[j] = max(c[j],row[j])
                    CAVE[Y-2-i] = c

        ROCKS = ROCKS + 1
    print(HEIGHT)

def part2():
    pass

part1()
part2()
