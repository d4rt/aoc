#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

muls = re.compile("mul\(([0-9]+),([0-9]+)\)")
do = re.compile("do\(\)")
dont = re.compile("don\'t\(\)")

def part1(lines):

    ins = [muls.findall(line) for line in lines]
    return sum([int(x)*int(y) for line in ins for x,y in line])


def part2(lines):
    prog = "".join(lines)
    enabled = True
    start = 0
    cont = True
    m = []
    while cont:
        switch = dont.search(prog, start)
        if switch:
            m.append(muls.findall(prog, start, switch.start()))
            switch_back = do.search(prog, switch.end())
            if switch_back:
                start = switch_back.end()
            else:
                cont = False
        else:
            m.append(muls.findall(prog,start))
            cont = False
    return sum([int(x) *int(y) for i in m for x,y in i])
            


def parse(lines):
    return lines


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
    if p1 == 161:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")

    print("Part 2")
    print("======")
    p2 = part2(test_parsed)
    if p2 == 48:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
