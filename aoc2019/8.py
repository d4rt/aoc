#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np

# from dataclasses import dataclass, field
# from functools import cache,lru_cache


def part1(image, width=25, height=6):
    layers = len(image) // (width * height)
    i = image.reshape((layers, height, width))
    ones = np.sum(np.count_nonzero(i == 1, axis=2), axis=1)
    twos = np.sum(np.count_nonzero(i == 2, axis=2), axis=1)
    nonzero = np.sum(np.count_nonzero(i, axis=2), axis=1)
    max_nonzero = nonzero.argmax()
    return ones[max_nonzero] * twos[max_nonzero]

def first_nontransparent(arr,axis):
    return np.where(arr.any(axis=axis),arr.argmax(axis=axis), -1)

def print_grid(grid):
    p_d = {0: ' ', 1: '█'}
    for l in grid:
        print(''.join([p_d[g] for g in l]))

def part2(image, width=25, height=6):
    layers = len(image) // (width * height)
    i = image.reshape((layers, height, width))
    not_transparent = i !=2
    assembled_image = np.zeros_like(i[0])
    for y in range(height):
        for x in range(width):
            for l in range(layers):
                if not_transparent[l][y][x]:
                    assembled_image[y][x] = i[l][y][x]
                    break
    print_grid(assembled_image)
    return assembled_image



def parse(lines):
    return np.array([int(c) for line in lines for c in line])


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


def test_part1():
    image = parse(["123456789012"])
    assert part1(image, width=3, height=2) == 1

def test_part2():
    image = parse(["0222112222120000"])
    assert np.all(part2(image,width=2, height=2) == np.array([[0,1],[1,0]]))
