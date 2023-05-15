#!/usr/bin/env python3
import sys
from enum import Enum
from functools import cmp_to_key

class Comparison(Enum):
    T = 1
    F = 2
    C = 3

def compare(a,b):
    for i,l in enumerate(a):
        if i >= len(b):
            return Comparison.F
        r = b[i]
        if type(l) == type(r) == int:
            if l<r:
                return Comparison.T
            if l>r:
                return Comparison.F
        if type(l) == list and type(r) == int:
            c = compare(l,[r])
            if c != Comparison.C:
                return c
        if type(l) == int and type(r) == list:
            c = compare([l],r)
            if c != Comparison.C:
                return c
        if type(l) == list and type(r) == list:
            if l == []:
                if r != []:
                   return Comparison.T
            else:
                c = compare(l,r)
                if c!= Comparison.C:
                    return c
    if len(a) == len(b):
        return Comparison.C
    if len(b) > len(a):
        return Comparison.T
    if len(a) > len(b):
        return Comparison.F
packets = [[[2]],[[6]]]

def cmp(r,l):
    c = compare(r,l)
    if c == Comparison.T:
        return -1
    if c == Comparison.F:
        return 1
    else:
        return 0

with open(sys.argv[1]) as infile:
    while(one := infile.readline().rstrip()):
        two = infile.readline().rstrip()
        b = infile.readline().rstrip()
        o = eval(one)
        t = eval(two)
        packets.append(o)
        packets.append(t)

sorted_packets = sorted(packets, key=cmp_to_key(cmp))


ans = 1
for i, p in enumerate(sorted_packets):
    if p == [[2]] or p == [[6]]:
        ans = ans * (i+1)

print(ans)
