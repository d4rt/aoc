#!/usr/bin/env python3

import sys

from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
def debug(s):
    pass

def part1(lines):
    raw_rules, updates = lines
    rules = defaultdict(list)

    for v,k in raw_rules:
        rules[k] += [v]

    sum = 0

    for update in updates:
        #debug(f"Update={update}")
        valid = True
        for idx, page in enumerate(update[:-1]):
            #debug(f"Checking page={page} against rules={rules[page]}")
            for before in rules[page]:
                if not valid:
                    break
                #debug(f"Checking before={before}")
                if before in update[idx:]:
                    #debug(f"Rule failed - update={update} rule={rules[page]} rule2={before}|{page} page={page} before={before} update[:idx]={update[:idx]}")
                    valid = False
            if not valid:
                break
        if valid:
            sum += update[len(update)//2]
            #debug(f"Valid - update={update} addition={update[len(update)//2]} sum={sum}")

    return sum

def fix(update, rules):
    debug(f"update:{update}")
    if len(update) == 1:
        return update
    fixed = []
    for idx, page in enumerate(update):
        if all([b not in update for b in rules[page]]):
            fixed.append(page)
            break
    assert len(fixed) > 0
    return fixed + fix(update[:idx] + update[idx+1:], rules)


def part2(lines):
    raw_rules, updates = lines
    rules = defaultdict(list)

    for v,k in raw_rules:
        rules[k] += [v]

    sum = 0

    for update in updates:
        #debug(f"Update={update}")
        valid = True
        for idx, page in enumerate(update[:-1]):
            #debug(f"Checking page={page} against rules={rules[page]}")
            for before in rules[page]:
                if not valid:
                    break
                #debug(f"Checking before={before}")
                if before in update[idx:]:
                    #debug(f"Rule failed - update={update} rule={rules[page]} rule2={before}|{page} page={page} before={before} update[:idx]={update[:idx]}")
                    valid = False
            if not valid:
                break
        if not valid:
            fixed = fix(update, rules)
            sum += fixed[len(fixed)//2]
            #debug(f"Fixed - update={update} addition={update[len(update)//2]} sum={sum}")

    return sum


def parse(lines):
    por, ppu = lines
    return ([list(map(int,p.split("|"))) for p in por], [list(map(int,p.split(","))) for p in ppu])


if __name__ == "__main__":
    test_infile = sys.argv[0][:-3] + "-test.txt"
    test_data = open(test_infile).read().strip()
 #   test_lines = [x for x in test_data.split("\n")]

    test_parsed = parse([x.split("\n") for x in test_data.split("\n\n")])

    infile = sys.argv[0][:-3] + "-input.txt"
    data = open(infile).read().strip()
    lines = [x.split("\n") for x in data.split("\n\n")]
    parsed = parse(lines)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 143:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 123:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
