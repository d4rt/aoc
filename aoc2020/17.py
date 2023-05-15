#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
#
def expand(cubes):
    return np.pad(cubes,((1,1),(1,1),(1,1)))

def expand4(cubes):
    return np.pad(cubes,((1,1),(1,1),(1,1),(1,1)))

def conway(cubes):
    cubes = expand(cubes)
    N = np.zeros_like(cubes)
    cubes = expand(cubes)
    # adapted from https://github.com/rougier/numpy-tutorial
    mz,my,mx = np.shape(cubes)
    for zf, zt in [(0,-2),(1,-1),(2,mz)]:
        for yf, yt in [(0,-2),(1,-1),(2,my)]:
            for xf, xt in [(0,-2),(1,-1),(2,mx)]:
                N += cubes[zf:zt,yf:yt,xf:xt]

    N -= cubes[1:-1,1:-1,1:-1]
    births = (N == 3) & (cubes[1:-1,1:-1,1:-1] == 0)
    survive = ((N == 2) | (N == 3)) & (cubes[1:-1,1:-1,1:-1] == 1)

    cubes[...] = 0
    cubes[1:-1,1:-1,1:-1][births | survive] = 1
    return cubes

def conway4(cubes):
    cubes = expand4(cubes)
    N = np.zeros_like(cubes)
    cubes = expand4(cubes)
    # adapted from https://github.com/rougier/numpy-tutorial
    mw,mz,my,mx = np.shape(cubes)
    for wf, wt in [(0,-2),(1,-1),(2,mz)]:
        for zf, zt in [(0,-2),(1,-1),(2,mz)]:
            for yf, yt in [(0,-2),(1,-1),(2,my)]:
                for xf, xt in [(0,-2),(1,-1),(2,mx)]:
                    N += cubes[wf:wt,zf:zt,yf:yt,xf:xt]

    N -= cubes[1:-1,1:-1,1:-1,1:-1]
    births = (N == 3) & (cubes[1:-1,1:-1,1:-1,1:-1] == 0)
    survive = ((N == 2) | (N == 3)) & (cubes[1:-1,1:-1,1:-1,1:-1] == 1)

    cubes[...] = 0
    cubes[1:-1,1:-1,1:-1,1:-1][births | survive] = 1
    return cubes
p = {0:'.', 1:'#'}

def trim_zeros(arr):
    """Returns a trimmed view of an n-D array excluding any outer
    regions which contain only zeros.
    """
    slices = tuple(slice(idx.min(), idx.max() + 1) for idx in np.nonzero(arr))
    return arr[slices]
def print3(c):
    t = trim_zeros(c)
    zi = len(t) //2
    for i, plane in enumerate(t):
        print(f"z={i - zi}")
        for y in plane:
            print(''.join([p[x] for x in y]))
def part1(cubes):
    cubes = np.pad(cubes,((1,1),(0,0),(0,0)))
    for i in range(6):
        cubes = conway(cubes)
        #print(f"After {i + 1} cycles:")
        #print3(cubes)
    return np.count_nonzero(cubes)

def part2(cubes):
    cubes = np.pad(cubes[np.newaxis,...],((1,1),(1,1),(0,0),(0,0)))
    for i in range(6):
        cubes = conway4(cubes)
    return np.count_nonzero(cubes)
d = {'.': 0, '#': 1}
def parse(lines):
    return np.array([[[d[x] for x in line] for line in lines]],dtype=int)

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
    if p1 == 112:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 848:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
