#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
import pytest

def dbg(s):
    print(s)
    # pass

def spoken(turns,numbers):
    history = {} # key : number spoken, val : turn spoken
    history2 = {} # key : number spoken, val : turn spoken
    first = True
    for t in tqdm(range(1, turns + 1)):
        if t <= len(numbers):
            s = numbers[t - 1]
        elif first:
            s = 0
        else:
            s = history[p] - history2[p]
        if s in history:
            first = False
            history2[s] = history[s]
        else:
            first = True
        history[s] = t
        #dbg(f"Turn {t}: {s} {first} {history[s] if not first else 0}")
        p = s
    return s

def part1(numbers):
    return spoken(2020,numbers)

def part2(numbers):
    return spoken(30_000_000, numbers)

def parse(lines):
    return [int(x) for line in lines for x in line.split(',') ]


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
    if p1 == 436:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 175594:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

@pytest.mark.parametrize("numbers,expected",[("0,3,6",436),("1,3,2",1),("2,1,3",10),("1,2,3",27),("2,3,1",78),("3,2,1",438),("3,1,2",1836)])
def test_2020(numbers,expected):
    assert part1(parse([numbers])) == expected

@pytest.mark.parametrize("numbers,expected",[("0,3,6",175594),("1,3,2",2578),("2,1,3",3544142),("1,2,3",261214),("2,3,1",6895259),("3,2,1",18),("3,1,2",362)])
def test_3m(numbers,expected):
    assert part2(parse([numbers])) == expected
