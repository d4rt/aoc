#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np
from numpy.linalg import matrix_power

def part1(poly):
    polymer, pairs = poly
    for step in range(10):
        new_polymer = ''
        for i in range(len(polymer) - 1):
            pair = polymer[i:i + 2]
            if pair in pairs:
                new_polymer += polymer[i] + pairs[pair]
            else:
                new_polymer += polymer[i]
        new_polymer += polymer[-1]
        polymer = new_polymer
        #print(f"After step {step + 1}: {polymer}")
    p_array = np.array(list(polymer))
    values, counts = np.unique(p_array, return_counts=True)
    counts.sort()
    return counts[-1] - counts[0]
def part2(poly):
    polymer, pairs = poly
    indexes = {p:i for i,p in enumerate(pairs.keys())} # map pairs to matrix rows/cols
    rev_indexes = {i:p for i,p in enumerate(pairs.keys())}
    matrix = np.zeros((len(pairs),len(pairs)),dtype=int)
    for i,p in enumerate(pairs.keys()):
       l = p[0]
       r = p[1]
       c = pairs[p]
       lp = l + c
       rp = c + r
       matrix[i][indexes[lp]] = 1
       matrix[i][indexes[rp]] = 1
    matrix_10 = matrix_power(matrix,10) # 10 steps
    matrix_40 = matrix_power(matrix,40) # 40 steps
    input_cvec = np.zeros((len(pairs)),dtype=int)
    for i in range(len(polymer) - 1):
        pair = polymer[i:i+2]
        input_cvec[indexes[pair]] += 1
    #input_cvec = np.atleast_2d(input_cvec).T
    polymer_10 = np.dot(matrix_10.T,input_cvec) # not sure why we had to transpose here? used dot product instead of matmul, not sure if both would work
    polymer_40 = np.dot(matrix_40.T,input_cvec)
    counts = {}
    # count each character - the column vector is for pairs
    for i, p in enumerate(polymer_40):
        l = rev_indexes[i][0]
        r = rev_indexes[i][1]
        if l in counts:
            counts[l] += p
        else:
            counts[l] = p
        if r in counts:
            counts[r] += p
        else:
            counts[r] = p
    counts[polymer[0]] += 1 # every element but first and last is double counted, so add these back in, so when halved it's correct
    counts[polymer[-1]] += 1
    counts = sorted(counts.values())
    return (counts[-1] - counts[0]) // 2 # halve because of the double counting

def parse(lines):
    polymer = lines[0]
    pairs = {l[:2] : l[6]  for l in lines[2:]}
    return (polymer,pairs)
test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]
test_parsed  = parse(test_lines)

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]
parsed  = parse(lines)

p1 = part1(test_parsed)
print("Part 1")
print("======")
if p1 == 1588:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 2188189693529:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
