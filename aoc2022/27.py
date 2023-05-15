#!/usr/bin/env python3

import sys
import numpy as np
paths = []

MIN_Y = MIN_X = 0
MAX_X = MAX_Y = 1
with open(sys.argv[1]) as infile:
    while(path := infile.readline().rstrip()):
        path_points = path.split(" -> ")
        paths.append(path_points)
        for p in path_points:
            (x,y) = [int(v) for v in p.split(',')]
            MIN_X = min(x,MIN_X)
            MAX_X = max(x,MAX_X)
            MAX_Y = max(y,MAX_Y)
ABYSS_Y = MAX_Y + 1
MAX_X = max(500,MAX_X)
MIN_X = min(500,MIN_X)

WORLD=np.zeros((MAX_X+2,MAX_Y+2))

for path in paths:
    for i, s in enumerate(path[:-1]):
        e = path[i+1]
        (sx,sy) = [int(v) for v in s.split(',')]
        (ex,ey) = [int(v) for v in e.split(',')]
        if sx==ex:
            mi = min(sy,ey)
            ma = max(sy,ey)
            for j in range(mi,ma + 1):
                WORLD[sx][j] = 1
        if sy==ey:
            mi = min(sx,ex)
            ma = max(sx,ex)
            for j in range(mi,ma+1):
                WORLD[j][sy] = 1
grains =0
sandy = 0
sandx = 500

while(True):
    if sandy >= ABYSS_Y:
        break
    # DOWN
    if WORLD[sandx][sandy+1] == 0:
        sandy = sandy + 1
        continue
    # DOWN + LEFT
    if WORLD[sandx-1][sandy+1] == 0:
        sandx = sandx - 1
        sandy = sandy + 1
        continue
    # DOWN + RIGHT
    if WORLD[sandx+1][sandy+1] == 0:
        sandx = sandx + 1
        sandy = sandy + 1
        continue
    # SETTLE
    WORLD[sandx][sandy] = 2
    sandx = 500
    sandy = 0
    grains = grains + 1

print(grains)
