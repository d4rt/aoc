#!/usr/bin/env python3

import sys
from collections import deque
import re

stacks = {}
re_s = re.compile(r"\[")
re_i = re.compile(r"move (?P<count>[0-9]+) from (?P<from>[0-9]+) to (?P<to>[0-9]+)")

with open(sys.argv[1]) as infile:
    while(line := infile.readline().rstrip()):
        if (re_s.search(line)):
            for stack, item in enumerate(line[1::4]):
                if not item == ' ':
                    stack = stack + 1
                    if stack in stacks:
                        stacks[stack].appendleft(item)
                    else:
                        stacks[stack] = deque(item)

    while(line := infile.readline().rstrip()):
        instructions = re_i.match(line)
        items = [stacks[int(instructions.group('from'))].pop() for _i in range(int(instructions.group('count')))]
        for item in items[::-1]:
            stacks[int(instructions.group('to'))].append(item)
top = ""
for stack in sorted(stacks):
    top = top + stacks[stack][-1]

print(top)
