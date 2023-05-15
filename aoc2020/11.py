#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def extend(array):
    shape = array.shape
    shape = (shape[0] + 2, shape[1] + 2)
    new_array = np.zeros(shape)
    new_array[1:-1,1:-1] = array
    return new_array

def next_state(seats):
    # adapted from https://github.com/rougier/numpy-tutorial#the-game-of-life
    occupied = np.zeros_like(seats)
    next_state  = seats.copy()
    occupied[seats == 2] = 1
    adjacent = (occupied[ :-2, :-2] + occupied[ :-2,1:-1] + occupied[ :-2,2:] +
                occupied[1:-1, :-2]                       + occupied[1:-1,2:] +
                occupied[2:  , :-2] + occupied[2:  ,1:-1] + occupied[2:  ,2:])
    new_seats = (adjacent == 0) & (seats[1:-1,1:-1] == EMPTY)
    empty = (adjacent >= 4) & (seats[1:-1,1:-1] == OCCUPIED)
    next_state[1:-1,1:-1][empty] = EMPTY
    next_state[1:-1,1:-1][new_seats] = OCCUPIED
    return next_state

def part1(seats):
    # extend seats by 1 in each dimension
    seats = extend(seats)
    next_seats = next_state(seats)
    while not (next_seats == seats).all():
        seats = next_seats
        next_seats = next_state(seats)
    return np.count_nonzero(seats == OCCUPIED)

def compute_adjacency(seats):
    vectors = [(y,x) for y in [-1,1,0] for x in [1,-1,0] if not x==y==0]
    adjacency = np.zeros_like(seats)
    max_x = len(seats[0]) - 1
    max_y = len(seats) - 1
    def check_vector(v,y,x):
        cy = v[0] + y
        cx = v[1] + x
        while True:
            if cx < 0 or cy < 0 or cy > max_y or cx > max_x:
                return 0
            if seats[cy][cx] == OCCUPIED:
                return 1
            if seats[cy][cx] == EMPTY:
                return 0
            cy += v[0]
            cx += v[1]

    iterator = np.nditer(seats, flags=['multi_index'])
    for p in iterator:
        idx = iterator.multi_index
        y = idx[0]
        x = idx[1]
        adjacency[idx] = sum([check_vector(v,y,x) for v in vectors])
    return adjacency

def next_state2(seats):
    occupied = np.zeros_like(seats)
    next_state  = seats.copy()
    occupied[seats == 2] = 1
    adjacent = compute_adjacency(seats)
    new_seats = (adjacent[1:-1,1:-1] == 0) & (seats[1:-1,1:-1] == EMPTY)
    empty = (adjacent[1:-1,1:-1] >= 5) & (seats[1:-1,1:-1] == OCCUPIED)
    next_state[1:-1,1:-1][empty] = EMPTY
    next_state[1:-1,1:-1][new_seats] = OCCUPIED
    return next_state

def part2(seats):
    # extend seats by 1 in each dimension
    seats = extend(seats)
    #print_grid(seats)
    next_seats = next_state(seats)
    #print_grid(next_seats)
    while not (next_seats == seats).all():
        seats = next_seats
        next_seats = next_state2(seats)
        #print_grid(next_seats)
    return np.count_nonzero(seats == OCCUPIED)

d = {'#': 2, 'L': 1, '.': 0}
p = {v:k for k,v in d.items()}
OCCUPIED = 2
EMPTY = 1
NOTHING = 0
def parse(lines):
    return np.array([[d[x] for x in line] for line in lines],dtype=int)
def print_grid(g):
    for row in g:
        print(''.join([p[x] for x in row]))
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
    if p1 == 37:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 26:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
