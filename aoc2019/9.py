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
    out = run(code,[1])
    return out[-2]


def part2(code):
    out = run(code,[2])
    return out[0]



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
