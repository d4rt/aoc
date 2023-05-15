#!/usr/bin/env python3

import sys
directions = { 'R': (0,1),
               'L': (0,-1),
               'U': (1,0),
               'D': (-1,0)}

head = [0,0]
tails = []
for i in range(9):
    tails.append([0,0])


tail_locations = {}

def direct_distance(h,t):
    if h[0] == t[0]:
        return abs(h[1] - t[1])
    if h[1] == t[1]:
        return abs(h[0] - t[0])
    return 0

def diagonal_distance(h,t):
    return abs(h[0] - t[0]) + abs(h[1] - t[1])

def print_diag(h,t):
    max_height = max(h[0],t[0])
    max_width = max(h[1],t[1])
    print()
    for j in reversed(range(max_height + 1)):
        row = ""
        for i in range(max_width + 1):
            char = '.'
            if i == 0 and j ==0 :
                char = 's'
            if t[0] == j and t[1] == i:
                char = "T"
            if h[0] == j and h[1] == i:
                char = "H"
            row = row + char
        print(row)
    print()

def move_tail(h,t):
    if direct_distance(h,t) == 2:
        t[0] = t[0] + directions[direction][0]
        t[1] = t[1] + directions[direction][1]
    if diagonal_distance(h,t) > 2:
        if t[0] > h[0]:
            u = -1
        else:
            u = 1
        if t[1] > h[1]:
            l = -1
        else:
            l = 1
        t[0] = t[0] + u
        t[1] = t[1] + l

with open(sys.argv[1]) as infile:
    while(line := infile.readline().rstrip()):
        direction, steps = line.split(' ')
        steps = int(steps)
        for i in range(steps):
            head[0] = head[0] + directions[direction][0]
            head[1] = head[1] + directions[direction][1]
            for j in range(9):
                if j == 0:
                    move_tail(head,tails[j])
                else:
                    move_tail(tails[j-1],tails[j])
            if (tails[8][0],tails[8][1]) not in tail_locations:
                tail_locations[(tails[8][0],tails[8][1])] = 1
print(len(tail_locations.items()))
