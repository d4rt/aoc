#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np

facings = {'r': 0, 'd': 1, 'l': 2, 'u': 3}
facings_direction = {'r': (1,0) , 'd': (0,1), 'l':(-1,0), 'u': (0,-1)}
facings_R = {'r': 'd', 'd': 'l', 'l':'u', 'u':'r'}
facings_L = {'r': 'u', 'u': 'l', 'l':'d', 'd':'r'}
facings_print = {'r': '>', 'd': 'V', 'u': '^', 'l':'<'}
X = 0 # col
Y = 1 # row
DIST = 0
TURN = 1
EMPTY = 0
ROCK = 1

def print_history(map,rocks,history):
    max_X = max([m[X] for m in map])
    max_Y = max([m[Y] for m in map])
    for y in range(max_Y+1):
        for x in range(max_X+1):
            c = ' '
            if (x,y) in map:
                c = '.'
            for h in history:
                if h[X] == x and h[Y] == y:
                    c = facings_print[h[2]]
            if (x,y) in rocks:
                c = '#'
            print(c,end='')
        print()

def part1(lines):
    l_map = lines[:-3]
    l_instructions = lines[-2]
    instructions = re.findall(r"(\d+)(R|L)?", l_instructions)
    map = set()
    rocks = set()
    for y, l in tqdm(enumerate(l_map)):
        for x, c in enumerate(l):
            if c != ' ':
                map.add((x,y))
            if c == '#':
                map.add((x,y))
                rocks.add((x,y))
    start_y = 0
    for m in map:
        start_x = min([m[X] for m in map if m[Y] == start_y ])

    x, y = (start_x, start_y)
    facing = 'r'
    history = [(x,y,facing)]
    for i in tqdm(instructions):
        vector = facings_direction[facing]
        for j in range(int(i[DIST])):
            new_x = x + vector[X]
            new_y = y + vector[Y]
            if (new_x, new_y) in rocks:
                break
            if (new_x, new_y) in map:
                x = new_x
                y = new_y
                history.append((x,y,facing))
            else:
                if vector[Y] == 1:
                    new_y = min([m[Y] for m in map if m[X] == new_x])
                elif vector[Y] == -1:
                    new_y = max([m[Y] for m in map if m[X] == new_x])
                elif vector[X] == 1:
                    new_x = min([m[X] for m in map if m[Y] == new_y])
                else:
                    new_x = max([m[X] for m in map if m[Y] == new_y])
                if (new_x,new_y) not in rocks and (new_x,new_y) in map:
                    x = new_x
                    y = new_y
                    history.append((x,y,facing))
                else:
                    break

        if i[TURN] == 'R':
            facing = facings_R[facing]
        if i[TURN] == 'L':
            facing = facings_L[facing]
    row = y + 1
    col = x + 1
    f = facings[facing]
    return (1000 * row + 4 * col + facings[facing])


m_dict = {'.': 0, '#': 1}
#facings = {'r': 0, 'd': 1, 'l': 2, 'u': 3}
p_dict = {0: '.', 1: '#'}

def print_map(map,history,rows,cols):
    cols_max = int(cols.max()) + 1
    rows_max = int(rows.max()) + 1
    p_map = [list(' ' * cols_max) for i in range(rows_max)]
    it = np.nditer(map,flags=['multi_index'])
    while not it.finished:
        r = rows[it.multi_index]
        c = cols[it.multi_index]
        p_map[r][c] = p_dict[int(it[0])]
        it.iternext()

    FACE = 0
    Y = 1
    X = 2
    FACING = 3
    for h in history:
        r = rows[h[:-1]]
        c = cols[h[:-1]]
        p_map[r][c] =  facings_print[h[FACING]]

    for r in p_map:
              print(''.join(r))

def face_transition_4(location):
    # which face to move to?
    face,y,x,facing = location
        #  0
        #123
        #  45
    d='x'
    if y == 4:
        d = 'd'
    if y == -1:
        d = 'u'
    if x == 4:
        d = 'r'
    if x == -1:
        d = 'l'
    if d == 'x':
        print(f"not an edge ? {location}")
        exit
    # which face (face,y,x,facing)
    face_0 = {'u': (1,0,3-x,'d'), 'd': (3,0,x,'d'), 'l': (2,0,y,'d'), 'r': (5,3-y,3,'l')}
    face_1 = {'u': (0,0,3-x,'d'), 'd': (4,3,3-x,'u'), 'l': (5,3,3-y,'u'), 'r': (2,y,0,'r')}
    face_2 = {'u': (0,x,0,'r'), 'd': (4,3-x,0,'r'), 'l': (1,y,3,'l'), 'r': (3,y,0,'r')}
    face_3 = {'u': (0,3,x,'u'), 'd': (4,0,x,'d'), 'l': (2,y,3,'l'), 'r': (5,0,3-y,'d')}
    face_4 = {'u': (3,3,x,'u'), 'd': (1,3,3-x,'u'), 'l': (2,3,3-y,'u'), 'r': (5,y,0,'r')}
    face_5 = {'u': (3,3-x,3,'l'), 'd': (1,3-x,0,'r'), 'l': (4,y,3,'l'), 'r': (0,3-y,3,'l')}

    faces = {0: face_0, 1: face_1, 2: face_2, 3: face_3, 4: face_4, 5: face_5}

    return faces[face][d]

def face_transition_50(location):
    # which face to move to?
    face,y,x,facing = location
        #  01
        #  2
        # 34
        # 5
    d='x'
    if y == 50:
        d = 'd'
    if y == -1:
        d = 'u'
    if x == 50:
        d = 'r'
    if x == -1:
        d = 'l'
    if d == 'x':
        print(f"not an edge ? {location}")
        exit
    # which face (face,y,x,facing)
    face_0 = {'u': (5,49-x,0,'r'), 'd': (2,0,x,'d'), 'l': (3,49-y,0,'r'), 'r': (1,y,0,'r')}
    face_1 = {'u': (5,49,x,'u'), 'd': (2,x,49,'l'), 'l': (0,y,49,'l'), 'r': (4,49-y,49,'l')}
    face_2 = {'u': (0,49,x,'u'), 'd': (4,0,x,'d'), 'l': (3,0,y,'d'), 'r': (1,49,y,'u')}
    face_3 = {'u': (2,x,0,'r'), 'd': (5,0,x,'d'), 'l': (0,49-y,0,'r'), 'r': (4,y,0,'r')}
    face_4 = {'u': (2,49,x,'u'), 'd': (5,x,49,'l'), 'l': (3,y,49,'l'), 'r': (1,49-y,49,'l')}
    face_5 = {'u': (3,49,x,'u'), 'd': (1,0,x,'d'), 'l': (0,0,y,'d'), 'r': (4,49,y,'u')}

    faces = {0: face_0, 1: face_1, 2: face_2, 3: face_3, 4: face_4, 5: face_5}

    return faces[face][d]
def part2(lines):
    l_map = lines[:-3]
    l_instructions = lines[-2]
    instructions = re.findall(r"(\d+)(R|L)?", l_instructions)
    if len(l_map[1]) == 12:
        width = 4
    else:
        width = 50
    if width == 4:
        #  0
        #123
        #  45
        # (face,row(y),col(x))
        face_transition = face_transition_4
        map = np.zeros((6,4,4),dtype=int)
        rows = np.zeros((6,4,4),dtype=int)
        cols = np.zeros((6,4,4),dtype=int)
        for y, l in enumerate(l_map[:4]):
            for x, c in enumerate(l.strip()):
                map[0,y,x] = m_dict[c]
                rows[0,y,x] = y + 1
                cols[0,y,x] = x + 9
        for y, l in enumerate(l_map[4:8]):
            for x,c in enumerate(l.strip()[:4]):
                map[1,y,x] = m_dict[c]
                rows[1,y,x] = y + 5
                cols[1,y,x] = x + 1
            for x,c in enumerate(l.strip()[4:8]):
                map[2,y,x] = m_dict[c]
                rows[2,y,x] = y + 5
                cols[2,y,x] = x + 5
            for x,c in enumerate(l.strip()[8:12]):
                map[3,y,x] = m_dict[c]
                rows[3,y,x] = y + 5
                cols[3,y,x] = x + 9
        for y, l in enumerate(l_map[8:12]):
            for x,c in enumerate(l.strip()[:4]):
                map[4,y,x] = m_dict[c]
                rows[4,y,x] = y + 9
                cols[4,y,x] = x + 9
            for x,c in enumerate(l.strip()[4:8]):
                map[5,y,x] = m_dict[c]
                rows[5,y,x] = y + 9
                cols[5,y,x] = x + 13
    if width == 50:
        #  01
        #  2
        # 34
        # 5
        # (face,row(y),col(x))
        print("width 50")
        face_transition = face_transition_50
        map = np.zeros((6,50,50),dtype=int)
        rows = np.zeros((6,50,50),dtype=int)
        cols = np.zeros((6,50,50),dtype=int)
        for y, l in enumerate(l_map[:50]):
            for x, c in enumerate(l.strip()[:50]):
                map[0,y,x] = m_dict[c]
                rows[0,y,x] = y + 1
                cols[0,y,x] = x + 51
            for x, c in enumerate(l.strip()[50:]):
                map[1,y,x] = m_dict[c]
                rows[1,y,x] = y + 1
                cols[1,y,x] = x + 101
        for y, l in enumerate(l_map[50:100]):
            for x,c in enumerate(l.strip()):
                map[2,y,x] = m_dict[c]
                rows[2,y,x] = y + 51
                cols[2,y,x] = x + 51
        for y,l in enumerate(l_map[100:150]):
            for x,c in enumerate(l.strip()[:50]):
                map[3,y,x] = m_dict[c]
                rows[3,y,x] = y + 101
                cols[3,y,x] = x + 1
            for x,c in enumerate(l.strip()[50:]):
                map[4,y,x] = m_dict[c]
                rows[4,y,x] = y + 101
                cols[4,y,x] = x + 51
        for y,l in enumerate(l_map[150:200]):
            for x,c in enumerate(l.strip()[:50]):
                map[5,y,x] = m_dict[c]
                rows[5,y,x] = y + 151
                cols[5,y,x] = x + 1


    FACE = 0
    Y = 1
    X = 2
    FACING = 3
    # test face mapping
    facings_test = {'r': [(2,width-1),(1,width-1)], 'l': [(1,0),(2,0)], 'u' : [(0,1),(0,2)], 'd': [(width-1,1),(width-1,2)] }
    for face in range(6):
        for facing in facings:
            print(f" Testing face {face} {facing}")
            for test in facings_test[facing]:
                location = (face,test[0],test[1],facing)
                new_location = list(location)

                if facing == 'r':
                    new_location[X] += 1
                if facing == 'l':
                    new_location[X] -= 1
                if facing == 'u':
                    new_location[Y] -= 1
                if facing == 'd':
                    new_location[Y] += 1
                new_location = tuple(new_location)
                print(f"location : {location} new location : {new_location}")
                new_location  = face_transition(new_location)
                print(f"warped to : {new_location}")
                history = [location,new_location]
                print_map(map,history,rows,cols)
    location = (0,0,0,'r')
    history = [location]
    for i in instructions:
        for j in range(int(i[DIST])):
            new_location = list(location)
            facing = location[FACING]
            if facing == 'r':
                new_location[X] += 1
            if facing == 'l':
                new_location[X] -= 1
            if facing == 'u':
                new_location[Y] -= 1
            if facing == 'd':
                new_location[Y] += 1
            new_location = tuple(new_location)
            if new_location[Y] == width or new_location[X] == width or new_location[Y] == -1 or new_location[X] == -1:
                print(new_location)
                new_location = face_transition(new_location)
                print(new_location)
            if map[new_location[:3]] == EMPTY:
                location = new_location
                history.append(location)
            else:
                break
        facing = location[FACING]
        if i[TURN] == 'R':
            facing = facings_R[facing]
        if i[TURN] == 'L':
            facing = facings_L[facing]
        location = tuple(list(location)[:3] + [facing])
        history.append(location)
    row = rows[location[:3]]
    col = cols[location[:3]]
    facing = location[3]
    return (1000 * row + 4 * col + facings[facing])

test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 6032:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 5031:
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
