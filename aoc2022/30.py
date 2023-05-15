#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

import numpy as np

infile = sys.argv[1] if len(sys.argv)>1 else (sys.argv[0][:-3] + '-test.txt')
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

re_s = re.compile("Sensor at x=(?P<sx>[-0-9]+), y=(?P<sy>[-0-9]+): closest beacon is at x=(?P<bx>[-0-9]+), y=(?P<by>[-0-9]+)")

sensors = []
beacons = []
distances = []
MAX_X = 0
MAX_Y = 0
MIN_X = 0
MIN_Y = 0

def distance(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

for l in lines:
    match = re_s.match(l)
    if(match):
        p = match.groupdict()
        sx = int(p['sx'])
        sy = int(p['sy'])
        bx = int(p['bx'])
        by = int(p['by'])
        sensors.append((sx,sy))
        beacons.append((bx,by))
        d= distance((sx,sy),(bx,by))
        distances.append(d)
        print(f" {p} : distance {d}")
        MAX_X = max(MAX_X,sx,bx)
        MIN_X = min(MIN_X,sx,bx)
        MAX_Y = max(MAX_Y,sy,by)
        MIN_Y = min(MIN_Y,sy,by)
print(len(sensors))
#Y = min(MAX_Y,2000000)
#Y = 10
#empty = 0
#for i in range(MIN_X,MAX_X):
#    e = any([ distance(s,(i,Y)) <= d for s,d in zip(sensors,distances)])
#    if e:
#        empty = empty + 1
#print(f"row: {Y} : {empty}")

#candidates = []
#for x in tqdm(range(4000000), desc="x"):
#    for y in range(4000000) :
#        e = all([ distance(s,(x,y)) > d for s,d in zip(sensors,distances)])
#        if e:
#           ss = x * 4000000 + y
#           print(ss)
#           break
x = 0
y = 0
SY = 4000000
e = False
t = tqdm(total=SY)
while(not e):
    m_r_dist = 1
    candidate = True
    for s,d in zip(sensors,distances):
        dist = distance(s,(x,y))
        if dist <= d:
            m_r_dist = max(d - dist, m_r_dist)
            candidate = False
    if candidate:
        print(x*4000000 + y)
        print(f"{x},{y}")
        for s, d in zip(sensors, distances):
            dist = distance(s, (x,y))
            print(f" sensors {s} sd {d} pd {dist} {dist>d}")
            e = True
    else:
        y = y + m_r_dist
    if y > SY:
        x = x + 1
        t.update(1)
        if x > SY:
            break
        y = 0
t.close()
def c(p):
    return (p[0]- MIN_X, p[1] - MIN_Y)
def o(p):
    return (p[0] + MIN_X, p[1] + MIN_Y)

print(f"{MIN_X},{MIN_Y},{MAX_X},{MAX_Y}")
TMAX_X = MAX_X+abs(MIN_X)
TMAX_Y = MAX_Y+abs(MIN_Y)

CAVE = np.zeros((TMAX_X+1,TMAX_Y+1))

UNKNOWN = 0
SENSOR = 1
BEACON = 2
EMPTY = 3

cave_dict = {UNKNOWN:".", SENSOR:"S", BEACON:"B", EMPTY:"#"}

def print_cave():
    print(f"{MIN_X},{MIN_Y},{MAX_X},{MAX_Y}")
    for j in range(TMAX_Y+1):
        print(''.join([cave_dict[x] for x in CAVE[:,j]]))
    print()

for s, b in zip(sensors,beacons):
    s = c(s) # translate
    b = c(b)
    CAVE[s[0],s[1]] = SENSOR
    CAVE[b[0],b[1]] = BEACON

print_cave()


for sensor, beacon in zip(sensors,beacons):
    d = distance(sensor, beacon)
    for i in range(d+1):
        for j in range(d+1-i):
            for (sgn_x,sgn_y) in [(1,1),(1,-1),(-1,-1),(-1,1)]:
                x = sensor[0] + sgn_x * j
                y = sensor[1] + sgn_y * i
                if x < TMAX_X and y < TMAX_Y:
                    if CAVE[x][y] == UNKNOWN:
                        CAVE[x][y] = EMPTY

print_cave()

# Part 1
TEST_ROW = min(MAX_Y,2000000)
u, c = np.unique(CAVE[:,c((0,TEST_ROW))[1]],return_counts=True)
rs = dict(zip(u,c))
print(rs[UNKNOWN])
