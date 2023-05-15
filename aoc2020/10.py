#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
from functools import cache,lru_cache

def part1(joltages):
    """If you *use every adapter in your bag* at once,
    what is the distribution of joltage differences between the charging outlet,
    the adapters, and your device?"""
    outlet = 0
    device = max(joltages) + 3
    joltages = sorted(joltages)
    joltages.append(device)
    one_diff = three_diff = 0
    current_joltage = outlet
    for jolts in joltages:
        diff = jolts - current_joltage
        # print(f"current {current_joltage}, jolts {jolts}, one {one_diff},three {three_diff}")
        if diff == 1:
            one_diff += 1
        elif diff == 3:
            three_diff += 1
        current_joltage = jolts
    return one_diff * three_diff
def part2(joltages):
    outlet = 0
    device = max(joltages) + 3
    joltages.append(outlet)
    joltages.append(device)
    joltages = sorted(joltages)

    @cache
    def permutations_from(joltage):
        permutations = 0
        if joltage == device:
            return 1
        for inc in [1,2,3]:
            if (joltage + inc) in joltages:
                permutations += permutations_from(joltage + inc)
        return permutations

    return permutations_from(outlet)

def parse(lines):
    """A list of all the joltage adapters in the bag"""
    return [int(l) for l in lines]

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
    if p1 == 7*5:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 8:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
