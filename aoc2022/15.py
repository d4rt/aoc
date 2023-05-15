#!/usr/bin/env python3
import sys

with open(sys.argv[1]) as infile:
       trees = infile.readlines()
x = len(trees)
y = len(trees[0]) - 1
visible = [[0 for col in range(x)] for row in range(y)]

for row in range(y):
    max_height = -1
    for col in range(x):
        height = int(trees[row][col])
        visible[row][col] = 1 * (height > max_height or visible[row][col] == 1)
        if height > max_height:
            max_height = height
    max_height = -1
    for col in reversed(range(x)):
        height = int(trees[row][col])
        visible[row][col] = 1 * (height > max_height or visible[row][col] == 1)
        if height > max_height:
            max_height = height

for col in range(x):
    max_height = -1
    for row in range(y):
        height = int(trees[row][col])
        visible[row][col] = 1 * (height > max_height or visible[row][col] == 1)
        if height > max_height:
            max_height = height
    max_height = -1
    for row in reversed(range(y)):
        height = int(trees[row][col])
        visible[row][col] = 1 * (height > max_height or visible[row][col] == 1)
        if height > max_height:
            max_height = height
visible_trees = 0

for row in range(y):
    for col in range(x):
        visible_trees = visible_trees + visible[row][col]
print(visible_trees)
