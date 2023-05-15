#!/usr/bin/env python3

import sys

from queue import PriorityQueue

# from collections import defaultdict, deque

# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache


def part1(orbits):
    direct_orbits = {o[1]: o[0] for o in orbits}
    orbits = 0
    for obj in direct_orbits:
        obj_orbits = 1
        obj = direct_orbits[obj]
        while obj != "COM":
            obj = direct_orbits[obj]
            obj_orbits += 1
        orbits += obj_orbits
    return orbits


def bfs(f, t, routes):
    visited = set()
    q = PriorityQueue()
    q.put((0, f, [f]))
    while not q.empty():
        d, loc, r = q.get()
        for n in routes[loc]:
            if n == t:
                return d + 1
            if n not in visited:
                visited.add(n)
                nr = r.copy()
                nr.append(n)
                q.put((d + 1, n, nr))


def to_graph(d):
    graph = dict()
    for key, item in d.items():
        if key not in graph:
            graph[key] = [item]
        else:
            graph[key].append(item)
        if item not in graph:
            graph[item] = [key]
        else:
            graph[item].append(key)
    return graph


def part2(orbits):
    transfers = to_graph({o[1]: o[0] for o in orbits})
    return bfs("YOU", "SAN", transfers) - 2


def parse(lines):
    return [line.split(")") for line in lines]


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
    if p1 == 54:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 4:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
