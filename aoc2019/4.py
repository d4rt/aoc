#!/usr/bin/env python3

import sys


# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
def valid(pw: str) -> bool:
    return adjacent(pw) and monotonic(pw)


def valid2(pw: str) -> bool:
    return adjacent2(pw) and monotonic(pw)


def adjacent(pw: str) -> bool:
    for i, j in zip(pw[:-1], pw[1:]):
        if i == j:
            return True
    return False


def adjacent2(pw: str) -> bool:
    for i, c in enumerate(pw[:-1]):
        pair = c == pw[i + 1]
        if pair:
            if i != 0:
                pair = pair and (pw[i - 1] != c)
            if (i + 2) <= len(pw) - 1:
                pair = pair and (pw[i + 2] != c)
            if pair:
                return True
    return False


def monotonic(pw: str) -> bool:
    for i, j in zip(pw[:-1], pw[1:]):
        if int(j) < int(i):
            return False
    return True


def part1(pw_range):
    return len(
        [pw for pw in range(int(pw_range[0]), int(pw_range[1]) + 1) if valid(str(pw))]
    )


def part2(pw_range):
    return len(
        [pw for pw in range(int(pw_range[0]), int(pw_range[1]) + 1) if valid2(str(pw))]
    )


def parse(lines):
    return lines[0].split("-")


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


def test_adj2():
    assert adjacent2("111122")
    assert not adjacent2("123444")
    assert adjacent2("112233")
    assert adjacent2("331331")
    assert adjacent2("333221")
    assert not adjacent2("333313")
    assert adjacent2("3331233")
    assert adjacent2("221122")
    assert not adjacent2("123789")
    assert adjacent2("221221")
    assert adjacent2("123433")
    assert adjacent2("444144")


def test_adj22():
    assert adjacent2("255666")
