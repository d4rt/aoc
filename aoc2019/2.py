#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from intcode import parse, run


def part1(code: list[int]) -> int:
    code[1] = 12
    code[2] = 2
    v = run(code)
    return v[0]


def part2(code):
    for noun in range(100):
        for verb in range(100):
            code[1] = noun
            code[2] = verb
            if run(code)[0] == 19690720:
                return 100 * noun + verb


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
    if p1 == 100:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 is None:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
