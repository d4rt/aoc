#!/usr/bin/env python3
import sys

elves = []
current = 0
max = 0
with open(sys.argv[1]) as infile:
    for line in infile:
       if line != '\n':
           current = current + int(line)
       else:
           elves.append(current)
           if current > max:
               max = current
           current = 0

print(max)
