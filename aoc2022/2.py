#!/usr/bin/env python3
import sys

elves = []
current = 0
with open(sys.argv[1]) as infile:
    for line in infile:
       if line != '\n':
           current = current + int(line)
       else:
           elves.append(current)
           current = 0

elves.sort(reverse=True)
print(sum(elves[0:3]))
