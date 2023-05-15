#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

from itertools import cycle
from copy import deepcopy
import math

infile = sys.argv[1] if len(sys.argv)>1 else (sys.argv[0][:-3] + '-test.txt')
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]
jet_dict = {'<': -1, '>' : 1}
jets = cycle([ jet_dict[x] for x in lines[0] ])

rocks = cycle([
    [[1,1,1,1]],
    [[0,1,0],
     [1,1,1],
     [0,1,0]],
    [[0,0,1],
     [0,0,1],
     [1,1,1]],
    [[1],
     [1],
     [1],
     [1]],
    [[1,1],
     [1,1]]
])
WIDTH = 7
FLOOR = 0

def apply_jet(jet, r, l, b,c):
    rock_width = len(r[0])
    new_l = l + jet
    new_l = max(0,new_l)
    new_l = min(new_l,WIDTH-rock_width)
    can_apply_jet = can_add_to_cave(r,new_l,b,c)
    if can_apply_jet:
        return new_l
    else:
        return l

def can_add_to_cave(rock,x,y,c):
    cave = [[0,0,0,0,0,0,0] for r in rock]
    for j, r in enumerate(reversed(rock)):
        rock_row = [0,0,0,0,0,0,0]
        rock_row[x:x+len(r)] = r
        cave[j] = [sum(i) for i in zip(c[y+j],rock_row)]
    return all([i < 2 for row in cave for i in row])

def add_to_cave(rock,x,y,c):
    # x is left, y is bottom
    # bottom is last element of rock
    for j, r in enumerate(reversed(rock)):
        rock_row = [0,0,0,0,0,0,0]
        rock_row[x:x+len(r)] = r
        c[y+j] = [sum(i) for i in zip(c[y+j],rock_row)]
    return c

def can_fall(r,l,b,c):
    b = b - 1
    return  can_add_to_cave(r,l,b,c)


def print_cave(c):
    c_d = {0:'.', 1:'#', 2:"X"}
    for row in reversed(range(len(c))):
        print(f"{row:05}  |" +  ''+(''.join([c_d[x] for x in c[row]]) + '|'))
    print("       +-------+")

def part1():
    CAVE = [[0,0,0,0,0,0,0] , [0,0,0,0,0,0,0]  ,[0,0,0,0,0,0,0] ]
    ROCKS = 1
    HEIGHT = 0
    while ROCKS < 2023:
        # get a new rock to drop
        rock = next(rocks)
        # rock starts falling from three above max height and 2 from the wall
        rock_left = 2
        rock_bottom = HEIGHT + 3
        rock_start  = rock_bottom
        falling = True
        # extend cave
        for i in range(rock_bottom + 1 + len(rock) - len(CAVE)):
            CAVE.append([0,0,0,0,0,0,0])
        # drop rock until it cannot any more
        while(falling):
            # apply jet
            jet = next(jets)
            rock_left = apply_jet(jet, rock, rock_left, rock_bottom, CAVE)
            # print_cave(add_to_cave(rock, rock_left, rock_bottom, CAVE))
            # check if can fall
            falling = can_fall(rock,rock_left,rock_bottom,CAVE)
            # if it can
            if(falling and rock_bottom > 0):
                # rock falls
                rock_bottom = rock_bottom - 1
            # if it cant
            else:
                # rock comes to rest
                CAVE = add_to_cave(rock, rock_left, rock_bottom, CAVE)
                # compute new height
                # height is highest row with a 1
                for i, row in enumerate(reversed(CAVE)):
                    if sum(row) > 0:
                        HEIGHT = len(CAVE) - i
                        break
                falling = False

        ROCKS = ROCKS + 1
    print(HEIGHT)

def part2():
    HEIGHT_HISTORY = [0]
    CAVE = [[0,0,0,0,0,0,0] , [0,0,0,0,0,0,0]  ,[0,0,0,0,0,0,0] ]
    ROCKS = 1
    GOAL = 1000000000000
    #GOAL = 2023
    JETS = 1
    HEIGHT = 0
    state_dict = {}
    cycle_dict = {}
    cycle = True
    t = tqdm(initial=1,total=GOAL)
    while ROCKS < GOAL:
        # get a new rock to drop
        rock = next(rocks)
        rock_cycle = ROCKS % 5
        # rock starts falling from three above max height and 2 from the wall
        rock_left = 2
        rock_bottom = HEIGHT + 3
        rock_start  = rock_bottom
        prev_height = HEIGHT
        falling = True
        # extend cave
        for i in range(rock_bottom + 1 + len(rock) - len(CAVE)):
            CAVE.append([0,0,0,0,0,0,0])
        #print_cave(CAVE)
        # drop rock until it cannot any more
        while(falling):
            # apply jet
            jet = next(jets)
            JETS = JETS + 1
            jet_cycle = JETS % len(lines[0])
            rock_left = apply_jet(jet, rock, rock_left, rock_bottom, CAVE)
            # print_cave(add_to_cave(rock, rock_left, rock_bottom, CAVE))
            # check if can fall
            falling = can_fall(rock,rock_left,rock_bottom,CAVE)
            # if it can
            if(falling and rock_bottom > 0):
                # rock falls
                rock_bottom = rock_bottom - 1
            # if it cant
            else:
                # rock comes to rest
                CAVE = add_to_cave(rock, rock_left, rock_bottom, CAVE)
                # compute new height
                # height is highest row with a 1
                for i, row in enumerate(reversed(CAVE)):
                    if sum(row) > 0:
                        HEIGHT = len(CAVE) - i
                        break
                falling = False

        HEIGHT_HISTORY.append(HEIGHT - prev_height)
        height_diff = HEIGHT_HISTORY[-1]
        if ROCKS == 2022:
            print(HEIGHT)
        # attempt to detect cycle
        if cycle:
            state = (rock_cycle,jet_cycle,height_diff)
            if state in state_dict:
                if state in cycle_dict:
                    # check is a true cycle
                    rocks_now_cycle = ROCKS - cycle_dict[state]['rocks']
                    rocks_cycle_state = cycle_dict[state]['rocks'] - state_dict[state]['rocks']

                    height_now_cycle = HEIGHT - cycle_dict[state]['height']
                    height_cycle_state = cycle_dict[state]['height'] - state_dict[state]['height']

                    if rocks_now_cycle == rocks_cycle_state and height_now_cycle == height_cycle_state:
                        print(f"{state}: {ROCKS} {HEIGHT} {state_dict[state]} {cycle_dict[state]}")
                        print(f"{HEIGHT_HISTORY[ROCKS]} {HEIGHT_HISTORY[ROCKS - rocks_now_cycle]} {HEIGHT_HISTORY[ROCKS- rocks_now_cycle - rocks_cycle_state]}")
                        if all([HEIGHT_HISTORY[i] - HEIGHT_HISTORY[i - rocks_now_cycle] == 0 for i in range(ROCKS - rocks_now_cycle + 1,ROCKS + 1) ]):

                            l = len(HEIGHT_HISTORY)

                            cycle_start = cycle_dict[state]['height']
                            cycle_period = HEIGHT - cycle_start
                            r = ROCKS - cycle_dict[state]['rocks']
                            cycles = (GOAL - ROCKS) // (r)
                            HEIGHT = cycle_start + ((cycles+1) * cycle_period ) # + remainder
                            ROCKS = ROCKS + (cycles * r)
                            to_go = GOAL - ROCKS
                            for i in range(state_dict[state]['rocks']+1,state_dict[state]['rocks'] + to_go+1):
                                HEIGHT = HEIGHT + HEIGHT_HISTORY[i]
                                ROCKS = ROCKS + 1
                            print(HEIGHT)
                            print(ROCKS)
                            cycle = False
                else:
                    cycle_dict[state] = {'rocks':ROCKS, 'height': HEIGHT}
            else:
                state_dict[state] = {'rocks':ROCKS, 'height': HEIGHT}
        ROCKS = ROCKS + 1
        t.update()
    print(HEIGHT)
#part1()
part2()
