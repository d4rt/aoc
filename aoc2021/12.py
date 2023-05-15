#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
# import numpy as np

def part1(graph):
    start = 'start'
    open_paths = deque([(['start'],['start'])])
    finished_paths = []
    while len(open_paths) > 0:
        path, visited_small = open_paths.popleft()
        for n in graph[path[-1]]:
           if n.islower() and n in visited_small:
               continue
           if n == 'end':
               p = path.copy()
               p.append(n)
               finished_paths.append(p)
           if n.islower():
               vs = visited_small.copy()
               vs.append(n)
               p = path.copy()
               p.append(n)
               open_paths.append((p,vs))
           else:
               p = path.copy()
               p.append(n)
               open_paths.append((p, visited_small))
    return len(finished_paths)
def part2(graph):
    start = 'start'
    open_paths = deque([(['start'],['start'],['start'])])
    finished_paths = []
    t = tqdm()
    while len(open_paths) > 0:
        t.update()
        path, visited_small,visited_small_twice = open_paths.popleft()
        for n in graph[path[-1]]:
           if n.islower() and n in visited_small_twice:
               continue
           if n.islower() and n in visited_small and len(visited_small_twice) < 2:
               p = path.copy()
               p.append(n)
               vst = visited_small_twice.copy()
               vst.append(n)
               open_paths.append((p,visited_small,vst))
               continue
           if n == 'end':
               p = path.copy()
               p.append(n)
               finished_paths.append(p)
               continue
           if n.islower() and n not in visited_small:
               vs = visited_small.copy()
               vs.append(n)
               p = path.copy()
               p.append(n)
               open_paths.append((p,vs,visited_small_twice))
           elif n.isupper():
               p = path.copy()
               p.append(n)
               open_paths.append((p, visited_small,visited_small_twice))
    return len(finished_paths)

def parse(lines):
    parsed = [x.split('-') for x in lines]
    graph = {}
    for f,t in parsed:
        if f in graph:
            graph[f].append(t)
        else:
            graph[f] = [t]
        if t in graph:
            graph[t].append(f)
        else:
            graph[t] = [f]
    return graph

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
if p1 == 10:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 36:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
