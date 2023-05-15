#!/usr/bin/env python3
import sys

with open(sys.argv[1]) as infile:
       trees_str = infile.readlines()
x = len(trees_str)
y = len(trees_str[0]) - 1
aesthetic = [[0 for col in range(x)] for row in range(y)]
aesthetic_debug = [[(0,0,0,0) for col in range(x)] for row in range(y)]

trees = [[int(trees_str[row][col]) for col in range(x)] for row in range(y)]

for row in range(y):
    for col in range(x):
        height = trees[row][col]
        l, r, u, d = (0, 0, 0, 0)
        for i in reversed(range(row)):
            if trees[i][col] < height:
                u = u + 1
            else:
                u = u + 1
                break
        height = trees[row][col]
        for i in range(row+1,y):
            if trees[i][col] < height:
                d = d + 1
            else:
                d = d + 1
                break
        height = trees[row][col]
        for i in reversed(range(col)):
            if trees[row][i] < height:
                l = l + 1
            else:
                l = l + 1
                break
        height = trees[row][col]
        for i in range(col+1,x):
            if trees[row][i] < height:
                r = r + 1
            else:
                r = r + 1
                break
        aesthetic[row][col] = l * r * u * d

aesthetic_trees = 0

for row in range(y):
    for col in range(x):
        if aesthetic[row][col] > aesthetic_trees:
            aesthetic_trees = aesthetic[row][col]

print(aesthetic_trees)
