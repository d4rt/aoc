#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from intcode import parse, run


def part1(code):
    output = run(code, intcode_input=[1])
    return output[-1]


def part2(code):
    output = run(code, intcode_input=[5])
    return output[-1]


if __name__ == "__main__":
    infile = sys.argv[0][:-3] + "-input.txt"
    data = open(infile).read().strip()
    lines = [x for x in data.split("\n")]
    parsed = parse(lines)
    print("Part 1")
    print("======")
    print(part1(parsed))

    print("Part 2")
    print("======")
    print(part2(parsed))
