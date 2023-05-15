#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

vectors = {'N': (1,0), 'S': (-1,0), 'E':(0,1), 'W':(0,-1)}
R_list = "NESW"
R_dict = {f:R_list[(ix + 1) % 4] for ix, f in enumerate(R_list) }
L_dict = {v:k for k,v in R_dict.items()}

def manhattan(f,t):
    return abs(t[0] - f[0]) + abs(t[1]-f[1])

def move(f,d,m):
    return (f[0] + m * d[0], f[1] + m * d[1])

def part1(directions):
    position = origin =  (0,0)
    orientation = 'E'
    for d in directions:
        if d[0] in R_list:
            position = move(position,vectors[d[0]],d[1])
        else:
            if d[0] == 'L':
                times = d[1] // 90
                for i in range(times):
                    orientation = L_dict[orientation]
            if d[0] == 'R':
                times = d[1] // 90
                for i in range(times):
                    orientation = R_dict[orientation]
            if d[0] == 'F':
                position = move(position,vectors[orientation], d[1])
    return manhattan(origin,position)

def part2(directions):
    position = origin =  (0,0)
    waypoint = (1,10)
    for d in directions:
        if d[0] in R_list:
            waypoint = move(waypoint,vectors[d[0]],d[1])
        if d[0] == 'L':
            # rotate left (counter-clockwise) about ship
            times = d[1] // 90
            for i in range(times):
                # (y,x) = (x, -y)
                waypoint = (waypoint[1],-waypoint[0])
        if d[0] == 'R':
            # rotate right (clockwise) about ship
            times = d[1] // 90
            for i in range(times):
                # (y,x) = (-x,y)
                waypoint = (-waypoint[1],waypoint[0])
        if d[0] == 'F':
            position = move(position,waypoint,d[1])
    return manhattan(origin,position)
def parse(lines):
    return [(l[0],int(l[1:])) for l in lines]

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
    if p1 == 25:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 286:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
