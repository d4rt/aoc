#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
from math import sqrt
# import numpy as np



def part1(coords):
    x_from, x_to, y_from, y_to = coords

    # * The probe's `x` position increases by its `x` velocity.
    # * The probe's `y` position increases by its `y` velocity.
    # * Due to drag, the probe's `x` velocity changes by `1` toward the value `0`; that is, it decreases by `1` if it is greater than `0`, increases by `1` if it is less than `0`, or does not change if it is already `0`.
    # * Due to gravity, the probe's `y` velocity decreases by `1`.
    #
    # pos_x = prev_pos_x + min(x_vec - t, 0)
    # pos_y = prev_pos_y + (y_vec - t)
    #
    # y reaches it's maximum when t = y_vec , i.e (y_vec * (y_vec + 1) ) / 2
    # x_vec must be at minimum enough to reach x_from, max_x will be 1/2 * (x_vec) * (x_vec + 1)
    # wolfram alpha solving in reverse gives  1/2 * (-1 +- sqrt(8*x + 1))
    #
    # first determine min x
    min_x_vec = int((-1 + sqrt(8 * x_from)) // 2)
    max_x_vec = int((-1 + sqrt(8 * x_to)) // 2) + 1
    min_y_vec = abs(y_to)
    max_y_vec = abs(y_from)
    best_max_y = 0
    for x_vec in range(min_x_vec, max_x_vec):
        for y_vec in range(min_y_vec, max_y_vec):
            # if we hit, store max height
            max_y = (y_vec * (y_vec + 1) ) / 2
            if max_y > best_max_y:
                # only check better than prior results
                #
                x_pos = 0
                y_pos = 0
                step = 0
                xv = x_vec
                yv = y_vec
                while True:
                   step += 1
                   x_pos += xv
                   y_pos += yv
                   xv = max(xv - 1,0)
                   yv = yv - 1
                   if x_from <= x_pos <= x_to and y_from <= y_pos <= y_to:
                       best_max_y = max_y
                       best_x_vec = x_vec
                       best_y_vec = y_vec
                       break
                   if x_pos > x_to:
                       break
                   if y_pos < y_to:
                       break
    print(f"x_vec {best_x_vec}, y_vec {best_y_vec}")
    return best_max_y
def part2(coords):
    x_from, x_to, y_from, y_to = coords
    min_x_vec = int((-1 + sqrt(8 * x_from)) // 2)
    max_x_vec = x_to
    min_y_vec = min(y_from,y_to)
    max_y_vec = max(abs(y_from),abs(y_to))
    print(min_x_vec,max_x_vec,min_y_vec,max_y_vec)
    count = 0
    for x_vec in range(min_x_vec, max_x_vec + 1):
        for y_vec in range(min_y_vec, max_y_vec + 1):
            x_pos = 0
            y_pos = 0
            step = 0
            xv = x_vec
            yv = y_vec
            while True:
                step += 1
                x_pos += xv
                y_pos += yv
                xv = max(xv - 1,0)
                yv = yv - 1
                if x_from <= x_pos <= x_to and y_from <= y_pos <= y_to:
                    count += 1
                    break
                if x_pos > x_to:
                    break
                if y_pos < y_from:
                    break
    return count

def parse(lines):
    re_target = re.compile("target area: x=(?P<x_from>-?\d+)\.\.(?P<x_to>-?\d+), y=(?P<y_from>-?\d+)\.\.(?P<y_to>-?\d+)")
    m = re_target.match(lines[0])
    d = m.groupdict()
    return (int(d['x_from']), int(d['x_to']), int(d['y_from']), int(d['y_to']))
test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]
test_parsed  = parse(test_lines)

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]
parsed  = parse(lines)

if __name__ == '__main__':
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 45:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 112:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
