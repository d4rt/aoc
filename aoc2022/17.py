#!/usr/bin/env python3

import sys
directions = { 'R': (0,1),
               'L': (0,-1),
               'U': (1,0),
               'D': (-1,0)}

head = [0,0]
tail = [0,0]

tail_locations = {}

def direct_distance(h,t):
    if h[0] == t[0]:
        return abs(h[1] - t[1])
    if h[1] == t[1]:
        return abs(h[0] - t[0])
    return 0

def diagonal_distance(h,t):
    return abs(head[0] - tail[0]) + abs(head[1] - tail[1])

def print_diag(h,t):
    max_height = max(head[0],tail[0])
    max_width = max(head[1],tail[1])
    print()
    for j in reversed(range(max_height + 1)):
        row = ""
        for i in range(max_width + 1):
            char = '.'
            if i == 0 and j ==0 :
                char = 's'
            if tail[0] == j and tail[1] == i:
                char = "T"
            if head[0] == j and head[1] == i:
                char = "H"
            row = row + char
        print(row)
    print()

with open(sys.argv[1]) as infile:
    while(line := infile.readline().rstrip()):
        direction, steps = line.split(' ')
        steps = int(steps)
        for i in range(steps):
            head[0] = head[0] + directions[direction][0]
            head[1] = head[1] + directions[direction][1]
            if direct_distance(head,tail) == 2:
                tail[0] = tail[0] + directions[direction][0]
                tail[1] = tail[1] + directions[direction][1]
            if diagonal_distance(head,tail) > 2:
                if tail[0] > head[0]:
                    u = -1
                else:
                    u = 1
                if tail[1] > head[1]:
                    l = -1
                else:
                    l = 1
                tail[0] = tail[0] + u
                tail[1] = tail[1] + l
            if (tail[0],tail[1]) not in tail_locations:
                tail_locations[(tail[0],tail[1])] = 1
print(len(tail_locations.items()))
