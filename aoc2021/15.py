#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np
def add_p(a,b):
    return tuple(i + j for i, j in zip(a,b))

Y = 0
X = 1

def part1(chitons):
    costs = np.zeros_like(chitons)
    start = (0,0)
    end = (len(chitons) - 1,len(chitons[0]) - 1)
    vecs = [(0,1),(1,0),(0,-1),(-1,0)]
    visited = set([start])
    node = start
    next_node_dict = {}
    while costs[end] == 0:
        for v in vecs:
            next_node = add_p(node, v)
            if 0 <= next_node[Y] <= end[Y] and 0 <= next_node[X] <= end[X] and next_node not in visited:
                costs[next_node] = costs[node] + chitons[next_node]
                visited.add(next_node)
                next_node_dict[next_node] = costs[next_node]
        sorted_next_nodes = sorted(next_node_dict.items(),key=lambda x:x[1]) # sort by cost ascending
        node = sorted_next_nodes[0][0]
        del next_node_dict[node]
    return costs[end]

def part2(minimap):
    chitons = np.tile(minimap,(5,5))
    Y = len(minimap)
    X = len(minimap[1])
    for y in range(5):
        for x in range(5):
            inc = (y + x) % 9
            chitons[y * Y:(y + 1) * Y, x * X : (x + 1) * X] += inc
            chitons[chitons>=10] -= 9
    costs = np.zeros_like(chitons)
    start = (0,0)
    end = (len(chitons) - 1,len(chitons[0]) - 1)
    vecs = [(0,1),(1,0),(0,-1),(-1,0)]
    visited = set([start])
    node = start
    next_node_dict = {}
    Y = 0
    X = 1
    while costs[end] == 0:
        for v in vecs:
            next_node = add_p(node, v)
            if 0 <= next_node[Y] <= end[Y] and 0 <= next_node[X] <= end[X] and next_node not in visited:
                costs[next_node] = costs[node] + chitons[next_node]
                visited.add(next_node)
                next_node_dict[next_node] = costs[next_node]
        sorted_next_nodes = sorted(next_node_dict.items(),key=lambda x:x[1]) # sort by cost ascending
        node = sorted_next_nodes[0][0]
        del next_node_dict[node]
    return costs[end]

def parse(lines):
    return np.array([[int(c) for c in line] for line in lines],dtype=int)
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
if p1 == 40:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 315:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
