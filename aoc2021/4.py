#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

def part1(lines):
    calls = deque([ int(x) for x in lines[0].split(',') ])
    n_boards = (len(lines) - 1) // 6
    boards = np.reshape(np.fromstring(' '.join(lines[2:]),dtype=int, sep=' '),(n_boards,5,5))
    marked = np.zeros((n_boards,5,5),dtype=bool)
    winner = False
    while not winner:
        call = calls.popleft()
        # mark board
        marked[boards == call] = True
        # check rows
        win_row = np.all(marked,axis = 1)
        win_check = np.where(win_row)
        for board, row in zip(win_check[0],win_check[1]):
            winner = board
            # check column
        win_column = np.all(marked,axis = 2)
        win_check = np.where(win_column)
        for board, col in zip(win_check[0],win_check[1]):
            winner = board
    return np.sum(boards[board] * ~marked[board]) * call


def part2(lines):
    calls = deque([ int(x) for x in lines[0].split(',') ])
    n_boards = (len(lines) - 1) // 6
    board_set = set(range(n_boards))
    boards = np.reshape(np.fromstring(' '.join(lines[2:]),dtype=int, sep=' '),(n_boards,5,5))
    marked = np.zeros((n_boards,5,5),dtype=bool)
    loser = False
    while not loser:
        call = calls.popleft()
        # mark board
        marked[boards == call] = True
        # check rows
        win_row = np.all(marked,axis = 1)
        row_winners = set(np.where(win_row)[0].flatten())
        # check column
        win_col = np.all(marked,axis = 2)
        col_winners = set(np.where(win_col)[0].flatten())
        remaining_boards = board_set - row_winners - col_winners
        if len(remaining_boards) == 1:
            losing_board = min(remaining_boards)
        if len(remaining_boards) == 0:
            loser = True

    return np.sum(boards[losing_board] * ~marked[losing_board]) * call
test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 4512:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 1924:
    print("Part 2")
    print("======")
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
