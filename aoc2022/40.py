#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import pytest

snafu_dict = {'1': 1, '2': 2, '0': 0, "-": -1, "=": -2}
rev_dict = {v:k for k,v in snafu_dict.items()}

def snafu2int(snafu):
    int = 0
    for i, c in enumerate(reversed(snafu)):
        int += snafu_dict[c] * (5 ** i)
    return int

def int2snafu(int):
    snafu = []
    while int > 0:
        cur = int % 5
        if cur <= 2:
            snafu.append(rev_dict[cur])
        else:
            cur = cur - 5
            snafu.append(rev_dict[cur])
        int = ((int - cur) / 5)
    return ''.join(reversed(snafu))

@pytest.mark.parametrize("snafu,int", [("1=-0-2", 1747),("12111", 906),("2=0=", 198),("21", 11),("2=01", 201),("111", 31),("20012", 1257),("112", 32),("1=-1=", 353),("1-12", 107),("12", 7),("1=", 3),("122", 37)])
def test_snafu2int(snafu, int):
    assert snafu2int(snafu) == int

@pytest.mark.parametrize("snafu,int", [("1=-0-2", 1747),("12111", 906),("2=0=", 198),("21", 11),("2=01", 201),("111", 31),("20012", 1257),("112", 32),("1=-1=", 353),("1-12", 107),("12", 7),("1=", 3),("122", 37)])
def test_int2snafu(snafu, int):
    assert int2snafu(int) == snafu

def part1(lines):
    return int2snafu(sum([snafu2int(l) for l in lines]))
def part2(lines):
    pass

if __name__ == '__main__':
    test_infile = sys.argv[0][:-3] + '-test.txt'
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split('\n')]

    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    lines = [x for x in data.split('\n')]

    p1 = part1(test_lines)
    if p1 == "2=-1=0":
        print("Part 1")
        print("======")
        print(p1)
        print(part1(lines))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_lines)
    if p2 == 0:
        print(p2)
        print(part2(lines))
    else:
        print(f"failed - {p1}")
