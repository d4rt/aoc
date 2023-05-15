#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def part1(groups):
    counts = []
    for group in groups:
        answers = set()
        for person in group:
            answers |= set(person)
        count = len(answers)
        counts.append(count)
    return sum(counts)

def part2(groups):
    counts = []
    for group in groups:
        answers = set(group[0])
        for person in group[1:]:
            answers &= set(person)
        count = len(answers)
        counts.append(count)
    return sum(counts)

def parse(data):
    groups = data.split('\n\n')
    return [ group.split('\n') for group in groups ]

if __name__ == '__main__':
    test_infile = sys.argv[0][:-3] + '-test.txt'
    test_data = open(test_infile).read().strip()
    test_parsed  = parse(test_data)

    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    parsed  = parse(data)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 11:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 6:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
