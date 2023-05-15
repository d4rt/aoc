#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache



def part1(passwords):
    valid = 0
    for f,t,c,pw in passwords:
        count = pw.count(c)
        if f <= count <= t:
            valid += 1
    return valid

def part2(passwords):
    valid = 0
    for f,t,c,pw in passwords:
        if ((pw[f - 1] == c) and (pw[t - 1] != c)) or ((pw[f - 1] != c) and (pw[t - 1] == c)):
            valid += 1
    return valid

def parse_line(line):
    rule, pw = line.split(":")
    pw = pw.strip()
    counts, c = rule.split(" ")
    f,t = counts.split("-")
    f = int(f)
    t = int(t)
    return (f,t,c,pw)

def parse(lines):
    return [parse_line(line) for line in lines]

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
    if p1 == 2:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 1:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
