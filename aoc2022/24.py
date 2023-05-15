#!/usr/bin/env python3

import sys
import numpy as np
from collections import deque

INFINITY = 30000

def height(c):
    if 97 <= ord(c) <= 122:
        return ord(c) - 96
    if c == 'S':
        return 1
    if c == 'E':
        return 26

def candidates(h,i,j):
    c = h[i][j]
    l = []
    if i > 0:
        if h[i-1][j] <= c + 1:
            l.append((i-1,j))
    if j > 0:
        if h[i][j-1] <= c + 1:
            l.append((i,j-1))
    if i + 1 < X:
        if h[i+1][j] <= c + 1:
            l.append((i+1,j))
    if j + 1 < Y:
        if h[i][j+1] <= c + 1:
            l.append((i,j+1))
    return l

with(open(sys.argv[1]) as infile):
    grid = infile.readlines()
    X = len(grid)
    Y = len(grid[0])-1
    heights = np.zeros((X,Y))
    starts = []
    for i in range(X):
        for j in range(Y):
            heights[i][j] = height(grid[i][j])
            if grid[i][j] == 'S' or grid[i][j] == 'a':
                starts.append((i,j))
            if grid[i][j] == 'E':
                end = (i,j)
    sedistances = []
    for start in starts:
        distances = np.full_like(heights,INFINITY)
        distances[start[0],start[1]] = 0
        current = start
        nexts = deque()
        nexts.append(start)
        while(current != end and len(nexts) > 0):
            current = nexts.popleft()
            cd = distances[current[0],current[1]]
            cs = candidates(heights,current[0],current[1])
            # print(f" current {current} distance {cd} candidates {cs}")
            for c in cs:
                if distances[c[0],c[1]] > cd + 1:
                    distances[c[0],c[1]] = cd + 1
                    nexts.append(c)
        sedistances.append(distances[end[0],end[1]])


print(min(sedistances))
