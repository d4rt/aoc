#!/usr/bin/env python3

import sys

from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache


def part1(lines):
    a,b = sorted([l[0] for l in lines]), sorted([l[1] for l in lines])
    answer = 0
    for i, j in zip(a,b):
        answer += abs(j-i)

    return answer



def part2(lines):
    a = [l[0] for l in lines]
    b = defaultdict(int)

    for i in [l[1] for l in lines]:
        b[i] += 1
    
    answer = 0
    
    for j in a:
        answer += j * b[j]

    return answer


def parse(lines):
    return [tuple(map(int,(line.split("   ")))) for line in lines] 


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
    if p1 == 11:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 31:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
