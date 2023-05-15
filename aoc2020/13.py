#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from math import gcd, prod

def part1(buses):
    time, buses, _ = buses
    wait = [bus - (time % bus) for bus in buses]
    minutes = min(wait)
    idx = wait.index(minutes)
    bus_id = buses[idx]
    return bus_id * minutes

def coprime(a: int,b:int ) -> bool:
    """
    a and b are coprime
    \( \gcd(a, b) = 1 \)
    """
    return gcd(a,b) == 1

def eaa(a: int,b: int) -> int:
    a0,a1,b0,b1 = 1,0,0,1

    while b > 0:
        g, a, b = a // b, b, a % b
        a0, a1 = a1, a0 - g * a1
        b0, b1 = b1, b0 - g * b1
    return b0


def crt(eqns: list) -> int:
    """
    find the solution (x) of the system of eqns where
    \( x \equiv  a_i (\mod n_i) \)

    \(N = \prod n_i \)

    \(y_i = \frac{N}{n_i}\)

    Applying Euclid's extended algorithm compute

    \(z_i \equiv y_{i}^{-1} (\mod n_i)\)

    """
    ni = [e[0] for e in eqns]
    ai = [e[1] for e in eqns]

    N =  prod(ni)
    yi = [ N // n for n in ni]

    zi = [eaa(ni[i],yi[i]) for i in range(len(ni)) ]

    x = sum([ai[i] * zi[i] * yi[i] for i in range(len(ni))])



    return (N - x) % N



def part2(buses):
    time, buses, buses_constraint =  buses
    multiplicand = 1
    test = []
    for offset, bus in enumerate(buses_constraint):
        if bus == 'x':
            continue
        else:
            test.append((bus, offset % bus))
    # apply chinese remainder theorem
    # verify all pairs are coprime
    assert all([coprime(a,b) for a in buses for b in buses if a != b])

    return crt(test)

        

def parse(lines):
    time = int(lines[0])
    buses = [int(x) for x in lines[1].split(',') if x.isnumeric()]
    buses_constraint = [int(x) if x.isnumeric() else x for x in lines[1].split(',')]
    return (time, buses, buses_constraint)

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
    if p1 == 295:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 1068781:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
