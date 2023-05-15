#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

infile = sys.argv[1] if len(sys.argv)>1 else (sys.argv[0][:-3] + '-test.txt')
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]
# x y z
cubes = set([tuple(map(int,x.split(','))) for x in lines])
(X, Y, Z) = (0, 1, 2)

def faces(cube,cubes):
    f = 6
    for adjacent in adjacency(cube,cubes):
        if adjacent in cubes:
            f = f - 1
    return f

def exterior_faces(cube,cubes,water):
    f = 6
    for adjacent in adjacency(cube,cubes):
        if adjacent in cubes or adjacent not in water:
            f = f - 1
    return f

def adjacency(cube,cubes):
    adjacency = [(1,0,0),(0,1,0),(0,0,1),
                 (-1,0,0),(0,-1,0),(0,0,-1)]
    return [(cube[X] + x, cube[Y] + y, cube[Z] + z) for x,y,z in adjacency]


def part1():
    return sum([faces(cube,cubes) for cube in cubes])

def exterior(cubes):
    # a cube is exterior if it's reachable in a straight line from the outside
    x_min = min([c[X] for c in cubes])
    y_min = min([c[Y] for c in cubes])
    z_min = min([c[Z] for c in cubes])
    x_max = max([c[X] for c in cubes])
    y_max = max([c[Y] for c in cubes])
    z_max = max([c[Z] for c in cubes])
    ext = []
    for y in range(y_min, y_max + 1):
        for z in range(z_min, z_max + 1):
            for x in range(x_min,x_max + 1):
                # mark first reached
                if (x,y,z) in cubes:
                    ext.append((x,y,z))
                    break # we only mark the first
            for x in reversed(range(x_min,x_max + 1)):
                if (x,y,z) in cubes:
                    if (x,y,z) not in ext:
                        ext.append((x,y,z))
                    break # we only mark the first
    for x in range(x_min, x_max + 1):
        for y in range(y_min,y_max + 1):
            for z in range(z_min, z_max + 1):
                if (x,y,z) in cubes:
                    if (x,y,z) not in ext:
                        ext.append((x,y,z))
                    break # we only mark the first
            for z in reversed(range(z_min, z_max + 1)):
                if (x,y,z) in cubes:
                    if (x,y,z) not in ext:
                        ext.append((x,y,z))
                    break # we only mark the first
    for x in range(x_min, x_max + 1):
        for z in range(z_min,z_max + 1):
            for y in range(y_min, y_max + 1):
                if (x,y,z) in cubes:
                    if (x,y,z) not in ext:
                        ext.append((x,y,z))
                    break # we only mark the first
            for y in reversed(range(y_min, y_max + 1)):
                if (x,y,z) in cubes:
                    if (x,y,z) not in ext:
                        ext.append((x,y,z))
                    break # we only mark the first
    return set(ext)
def air_pocket(cubes):
    # an air pocket exists where it can't be reached from the outside in a straight line
    x_min = min([c[X] for c in cubes])
    y_min = min([c[Y] for c in cubes])
    z_min = min([c[Z] for c in cubes])
    x_max = max([c[X] for c in cubes])
    y_max = max([c[Y] for c in cubes])
    z_max = max([c[Z] for c in cubes])
    air_x_1 = set()
    air_x_2 = set()
    air_y_1 = set()
    air_y_2 = set()
    air_z_1 = set()
    air_z_2 = set()
    OUTSIDE = 0
    INSIDE = 1
    for y in range(y_min, y_max + 1):
        for z in range(z_min, z_max + 1):
            state = OUTSIDE
            for x in range(x_min,x_max + 1):
                if OUTSIDE and (x,y,z) in cubes:
                    state = INSIDE
                    continue
                if INSIDE and (x,y,z) not in cubes:
                    air_x_1.add((x,y,z))
            state = OUTSIDE
            for x in reversed(range(x_min,x_max + 1)):
                if OUTSIDE and (x,y,z) in cubes:
                    state = INSIDE
                    continue
                if INSIDE and (x,y,z) not in cubes:
                    air_x_2.add((x,y,z))
    for x in range(x_min, x_max + 1):
        for y in range(y_min,y_max + 1):
            state = OUTSIDE
            for z in range(z_min, z_max + 1):
                if OUTSIDE and (x,y,z) in cubes:
                    state = INSIDE
                    continue
                if INSIDE and (x,y,z) not in cubes:
                    air_z_1.add((x,y,z))
            state = OUTSIDE
            for z in reversed(range(z_min, z_max + 1)):
                if OUTSIDE and (x,y,z) in cubes:
                    state = INSIDE
                    continue
                if INSIDE and (x,y,z) not in cubes:
                    air_z_2.add((x,y,z))
    for x in range(x_min, x_max + 1):
        for z in range(z_min,z_max + 1):
            state = OUTSIDE
            for y in range(y_min, y_max + 1):
                if OUTSIDE and (x,y,z) in cubes:
                    state = INSIDE
                    continue
                if INSIDE and (x,y,z) not in cubes:
                    air_y_1.add((x,y,z))
            state = OUTSIDE
            for y in reversed(range(y_min, y_max + 1)):
                if OUTSIDE and (x,y,z) in cubes:
                    state = INSIDE
                    continue
                if INSIDE and (x,y,z) not in cubes:
                    air_y_1.add((x,y,z))
    print(air_x_1)
    return air_x_1 & air_x_2 & air_y_1 & air_y_2 & air_z_1 & air_z_2

def water_cube(cube):
    x_min = min([c[X] for c in cubes]) - 1
    y_min = min([c[Y] for c in cubes]) - 1
    z_min = min([c[Z] for c in cubes]) - 1
    x_max = max([c[X] for c in cubes]) + 1
    y_max = max([c[Y] for c in cubes]) + 1
    z_max = max([c[Z] for c in cubes]) + 1
    water = set([(x_min,y_min,z_min)])
    flood = deque([(x_min,y_min,z_min)])
    adjacency = [(1,0,0),(0,1,0),(0,0,1),
                 (-1,0,0),(0,-1,0),(0,0,-1)]
    while(len(flood)>0):
        c = flood.popleft()
        for d in adjacency:
            t = (c[X]+d[X],c[Y]+d[Y],c[Z]+d[Z])
            if t not in water and t not in cube and x_min <= t[X] <= x_max and y_min <= t[Y] <= y_max and z_min <= t[Z] <= z_max:
                flood.append(t)
                water.add(t)
    return water

def part2():
    water = water_cube(cubes)
    return sum([exterior_faces(cube,cubes,water) for cube in cubes])


print(part1())
print(part2())
