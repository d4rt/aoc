#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache


def part1(reports):
    return sum([safe_part1(report) for report in reports])


def safe_part1(report):
    ascending = False
    if report[0] == report[1]:
        return 0
    if report[0] < report[1]:
        ascending = True
    if report[0] > report[1]:
        ascending = False
    for i, j in zip(report[:-1],report[1:]):
        diff = 0 < abs(i-j) <= 3
        asc = (i < j and ascending)
        desc = (i > j and not ascending)
        if not (diff and (asc or desc)):
            return 0
    return 1

def part2(reports):
   return sum([safe_part2(report) for report in reports])

def safe_part2(report):
    safe = safe_part1(report)
    if safe == 1:
        return 1
    else:
        for i in range(len(report)):
            safe = safe_part1(report[:i]+report[i+1:])
            if safe == 1:
                return 1
            
    return 0


def parse(lines):
    reports = [line.split(" ") for line in lines]
    return [[int(x) for x in r] for r in reports]



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
    if p1 == 2:
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
