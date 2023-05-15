#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
# import numpy as np

def part1(lines):
    char_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    openings = "([{<"
    closings = {')':'(', ']':'[', '}':'{', '>':'<'}
    corruption = 0
    for line in lines:
        stack = []
        for char in line:
            if char in openings:
                stack.append(char)
            if char in closings:
                o = stack.pop()
                corrupted = not o == closings[char]
                if corrupted:
                    break
        # corrupted
        if corrupted:
            corruption += char_scores[char]
    return corruption
def part2(lines):
    openings = "([{<"
    closings = {')':'(', ']':'[', '}':'{', '>':'<'}
    completion = {v: i + 1 for i, v in enumerate(openings)}
    corruption = 0
    completions = []
    for line in lines:
        stack = []
        for char in line:
            if char in openings:
                stack.append(char)
            if char in closings:
                o = stack.pop()
                corrupted = not o == closings[char]
                if corrupted:
                    break
        if not corrupted:
            #incomplete?
            line_completion = 0
            for c in reversed(stack):
                line_completion *= 5
                line_completion += completion[c]
            completions.append(line_completion)
    completions = sorted(completions)
    return completions[(len(completions)//2)]

def parse(lines):
    return lines
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
if p1 == 26397:
    print(p1)
    print(part1(parsed))
else:
    print(f"failed - {p1}")
p2 = part2(test_parsed)
print("Part 2")
print("======")
if p2 == 288957:
    print(p2)
    print(part2(parsed))
else:
    print(f"failed - {p2}")
