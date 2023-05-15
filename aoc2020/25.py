#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def part1(keys):
    card_pubkey = keys[0]
    door_pubkey = keys[1]

    card_value = 1
    card_subject = 7
    card_secret_loop = 0
    while card_value != card_pubkey:
        card_secret_loop += 1
        card_value *= card_subject
        card_value %= 20201227
    door_value = 1
    door_subject = 7
    door_secret_loop = 0
    while door_value != door_pubkey:
        door_secret_loop += 1
        door_value *= card_subject
        door_value %= 20201227

    card_subject = door_pubkey
    card_value = 1
    for _ in range(card_secret_loop):
        card_value *= card_subject
        card_value %= 20201227
    return card_value
def part2(lines):
    pass

def parse(lines):
    return [int(x) for x in lines]

if __name__ == '__main__':
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
    if p1 == 14897079:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 5:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
