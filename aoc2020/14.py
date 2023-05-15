#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def part1(instructions):
    mem = defaultdict(int)
    for i in instructions:
        if i[0] == 'mask':
            m1 = i[1]
            m0 = i[2]
        if i[0] == 'mem':
            addr = i[1]
            val = i[2]
            masked_val = (val | m1) & ~m0
            mem[addr] = masked_val
    return sum(mem.values())

def set_bit(v,n):
    return v | ( 1 << n )
def get_bit(v,n):
    return ((v >> n & 1) != 0)
def clear_bit(v,n):
    return v & ~(1 << n)

def f36(b):
    return format(b,'#036b')
def p36(b):
    print(f36(b))

def permute(i: int) -> list[int]:
    combinations = [0]
    pow = -1
    while i > 0:
        lsb = i % 2
        pow += 1
        if lsb == 1:
            combinations.extend([c + 2 ** pow for c in combinations])
        i = i // 2
    return combinations


def part2(instructions):
    mem = defaultdict(int)
    for i in instructions:
        if i[0] == 'mask':
            m1 = i[1]
            m0 = i[2]
            mx = i[3]
            smx = permute(mx)
        if i[0] == 'mem':
            addr = i[1]
            val = i[2]
            addr = (addr & ~mx)
            addr = (addr | m1)
            for i in smx:
                mem[addr + i] = val
    return sum(mem.values())


def parse(lines):
    instructions = []
    for line in lines:
        i, v = line.split(' = ')
        if i == 'mask':
            m1 = int(v.replace('X','0'),2) # put 1 where this is 1
            m0 = int(v.replace('1', 'X').replace('0','1').replace('X','0'),2) # put 0 where this is 1
            mx = int(v.replace('1', '0').replace('X','1'),2) # put 1 where this is X
            instructions.append((i,m1,m0,mx))
        else:
            addr = int(i[4:].split(']')[0])
            val = int(v)
            instructions.append(('mem',addr,val))
    return instructions

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
    if p1 == 51:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    print("Part 2")
    print("======")
    p2 = part2(test_parsed)
    if p2 == 208:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
