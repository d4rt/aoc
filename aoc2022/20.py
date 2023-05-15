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

def render(cycle,x):
    pixel = (cycle % 40) - 1
    if x in [pixel-1,pixel,pixel+1]:
        crt = '#'
    else:
        crt = '.'
    # print(f" cycle {cycle} x {x} pixel {pixel} crt {crt}")
    return crt


CRT = [ render(i+1,X_history[i]) for i in range(240) ]
print(''.join(CRT[0:40]))
print(''.join(CRT[40:80]))
print(''.join(CRT[80:120]))
print(''.join(CRT[120:160]))
print(''.join(CRT[160:200]))
print(''.join(CRT[200:240]))

print(X_history[:22])
#signal_strength = 0
#for i in range(20,cycles,40):
#    print (f"i {i} x {X_history[i]} ss {i * X_history[i]}")
#    signal_strength = signal_strength + i * X_history[i-1]

#print(signal_strength)

#for i in range(20,cycles,40):
#    print (f"i {i-1} x {X_history[i-1]} ss {i-1 * X_history[i-1]}")
#    print (f"i {i} x {X_history[i]} ss {i * X_history[i]}")
#    print (f"i {i+1} x {X_history[i+1]} ss {(i+1) * X_history[i+1]}")
