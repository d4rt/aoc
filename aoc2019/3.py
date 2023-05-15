#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from operator import add


def part1(wires: list[list[tuple[str, int]]]) -> int:
    wire1 = set()
    location = (0, 0)
    vec = {"U": (1, 0), "D": (-1, 0), "L": (0, 1), "R": (0, -1)}
    for ins in wires[0]:
        direction = vec[ins[0]]
        for _ in range(ins[1]):
            location = tuple(map(add, location, direction))
            wire1.add(location)
    wire2 = set()
    location = (0, 0)
    for ins in wires[1]:
        direction = vec[ins[0]]
        for _ in range(ins[1]):
            location = tuple(map(add, location, direction))
            wire2.add(location)
    intersection = wire1 & wire2
    return min([abs(p[0]) + abs(p[1]) for p in intersection])


def part2(wires):
    wire1 = set()
    w1_times = {}
    location = (0, 0)
    time = 0
    vec = {"U": (1, 0), "D": (-1, 0), "L": (0, 1), "R": (0, -1)}
    for ins in wires[0]:
        direction = vec[ins[0]]
        for _ in range(ins[1]):
            time += 1
            location = tuple(map(add, location, direction))
            wire1.add(location)
            w1_times[location] = time
    wire2 = set()
    w2_times = {}
    location = (0, 0)
    time = 0
    for ins in wires[1]:
        direction = vec[ins[0]]
        for _ in range(ins[1]):
            time += 1
            location = tuple(map(add, location, direction))
            wire2.add(location)
            w2_times[location] = time
    intersection = wire1 & wire2
    return min([w1_times[p] + w2_times[p] for p in intersection])
    pass


def parse(lines):
    return [[(ins[0], int(ins[1:])) for ins in line.split(",")] for line in lines]


if __name__ == "__main__":
    test_infile = sys.argv[0][:-3] + "-test.txt"
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split("\n")]
    test_parsed = parse(test_lines)

    infile = sys.argv[0][:-3] + "-input.txt"
    data = open(infile).read().strip()
    lines = [x for x in data.split("\n")]
    parsed = parse(lines)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 135:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 410:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
