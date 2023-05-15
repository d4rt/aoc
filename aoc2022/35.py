#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

infile = sys.argv[1] if len(sys.argv)>1 else (sys.argv[0][:-3] + '-test.txt')
data = open(infile).read().strip()



def part1():
    ints = [int(x) for x in data.split('\n')]
    positions = list(range(len(ints)))
    l = len(ints)
    for i in range(l):
        pos = positions.index(i)
        val = ints[pos]
        new_pos = (pos + val) % (l - 1)
        v = ints.pop(pos)
        ints.insert(new_pos,v)
        j = positions.pop(pos)
        positions.insert(new_pos,i)
    loc = ints.index(0)
    print(sum([ints[(loc + 1000) % l], ints[(loc + 2000) % l], ints[(loc + 3000) % l]]))

def part2():
    key = 811589153
    ints = [int(x) * key for x in data.split('\n')]
    positions = list(range(len(ints)))
    l = len(ints)
    for round in range(10):
        for i in range(l):
            pos = positions.index(i)
            val = ints[pos]
            new_pos = (pos + val) % (l - 1)
            v = ints.pop(pos)
            ints.insert(new_pos,v)
            j = positions.pop(pos)
            positions.insert(new_pos,i)
    loc = ints.index(0)
    print(sum([ints[(loc + 1000) % l], ints[(loc + 2000) % l], ints[(loc + 3000) % l]]))


part1()
part2()
