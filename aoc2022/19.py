#!/usr/bin/env python3

import sys
import re

re_noop = re.compile(r"noop")
re_addx = re.compile(r"addx (?P<op>[-0-9]+)")

cycles = 0
X = 1
X_history = []
with open(sys.argv[1]) as infile:
    while(line := infile.readline().rstrip()):
        match = re_noop.match(line)
        if match:
            cycles = cycles + 1
            X_history.append(X)
        match = re_addx.match(line)
        if match:
            cycles = cycles + 2
            X_history.append(X)
            X_history.append(X)
            X = X + int(match.group('op'))

X_history.append(X)

signal_strength = 0
for i in range(20,cycles,40):
#    print (f"i {i} x {X_history[i]} ss {i * X_history[i]}")
    signal_strength = signal_strength + i * X_history[i-1]

print(signal_strength)

#for i in range(20,cycles,40):
#    print (f"i {i-1} x {X_history[i-1]} ss {i-1 * X_history[i-1]}")
#    print (f"i {i} x {X_history[i]} ss {i * X_history[i]}")
#    print (f"i {i+1} x {X_history[i+1]} ss {(i+1) * X_history[i+1]}")
