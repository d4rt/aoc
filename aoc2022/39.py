#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np
from copy import deepcopy

EMPTY = 0
WALL = 1
m_dict = {'.': EMPTY, '#': WALL}
w_dict = {'>': 0, '<': 1, '^': 2, 'v': 3}
m_dir = {0:(0,1), 1:(1,0), 2:(0,-1), 3:(-1,0), 4: (0,0)}
p_dict = {v:k for k,v in m_dict.items()}
ROW = 0
COL = 1

def make_map(lines):
    rows = len(lines)
    cols = len(lines[0])
    map = np.zeros((rows,cols),dtype=int)
    winds = np.zeros((5,rows,cols),dtype=int)
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c in w_dict:
                winds[w_dict[c],row,col] = 1
            else:
                map[row,col] = m_dict[c]
    return (map,winds)

def draw_map(map, winds, step, loc=None):
    rows,cols = np.shape(map)
    wind_rows = rows - 2
    wind_cols = cols - 2
    print(f"Minute {step}")
    for rn, r in enumerate(map):
        line = list(" " * len(r))
        for cn, c in enumerate(r):
            if c == WALL:
                line[cn] = "#"
            elif loc and loc[ROW] == rn and loc[COL] == cn:
                line[cn] = 'E'
            else:
                if winds[0,rn,((cn - 1 - step) % wind_cols) + 1 ] == 1:
                    line[cn] = '>'
                if winds[1,rn,((cn - 1 + step) % wind_cols) + 1] == 1:
                    if line[cn] == ' ':
                        line[cn] = '<'
                    else:
                        line[cn] = '2'
                if winds[2,((rn - 1 + step) % wind_rows) + 1, cn] == 1:
                    if line[cn] == " ":
                        line[cn] = "^"
                    elif line[cn] == '2':
                        line[cn] = '3'
                    elif line[cn] == '<' or line[cn] == '>':
                        line[cn] = '2'
                if winds[3,((rn - 1 - step) % wind_rows + 1), cn] == 1:
                    if line[cn] == " ":
                        line[cn] = "v"
                    elif line[cn] == '3':
                        line[cn] = '4'
                    elif line[cn] == '2':
                        line[cn] == '3'
                    else:
                        print(f"{line[cn]}")
                        line[cn] = '2'
        print(''.join(line))
    print()


def bfs(map,winds,step,pos,goal):
    rows,cols = np.shape(map)
    wind_rows = rows - 2
    wind_cols = cols - 2
    #queue = deque([(step,pos,[pos])])
    queue = deque([(step,pos)])
    t  = tqdm()
    max_step = 0
    while True:
        #step, pos, history = queue.popleft()
        step, pos = queue.popleft()
        n = step + 1
        if step > max_step:
            max_step = step
            t.update()
        if pos == goal:
            #for s, l in enumerate(history):
            #    draw_map(map,winds,s,l)
            return step
        for d in range(5):
            rv, cv = m_dir[d]
            r = pos[ROW] + rv
            c = pos[COL] + cv
            if (n,(r,c)) not in queue:
                if r < rows and c < cols and map[r][c] == EMPTY:
                    # > (0), < (1), ^ (2), v (3)
                    if (winds[0,r,((c - 1 - n) % wind_cols) + 1] == 0 and
                        winds[1,r,((c - 1 + n) % wind_cols) + 1] == 0 and
                        winds[2,((r - 1 + n) % wind_rows) + 1,c] == 0 and
                        winds[3,((r - 1 - n) % wind_rows) + 1,c] == 0):
                        #new_history = deepcopy(history)
                        #new_history.append((r,c))
                        queue.append((n,(r,c))) #,new_history))

def part1(lines):
    map, winds = make_map(lines)
    rows,cols = np.shape(map)
    return bfs(map,winds,0,(0,1),(rows - 1, cols - 2))
def part2(lines):
    map, winds = make_map(lines)
    rows,cols = np.shape(map)
    step = bfs(map,winds,0,(0,1),(rows - 1, cols - 2))
    step = bfs(map,winds,step,(rows - 1, cols - 2), (0,1))
    step = bfs(map,winds,step,(0,1),(rows - 1, cols - 2))
    return step



test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 18:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 54:
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
