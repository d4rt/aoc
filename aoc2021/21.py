#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
from itertools import cycle

def part1(positions):
    p1_pos, p2_pos = positions
    p1_score = 0
    p2_score = 0
    rolls = 0
    roll = cycle(range(1,101))
    while p2_score < 1000:
        p1_pos += sum([next(roll) for i in range(3)])
        rolls = rolls + 3
        p1_pos = ((p1_pos - 1 ) % 10 ) + 1
        p1_score += p1_pos
        if p1_score >= 1000:
            break
        p2_pos += sum([next(roll) for i in range(3)])
        rolls = rolls + 3
        p2_pos = ((p2_pos - 1 ) % 10 ) + 1
        p2_score += p2_pos
    return min(p1_score,p2_score) * rolls

def gen_dirac_dict(rolls):
    res = {i:0 for i in range(3,10)}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                res[i + j + k + 3] += 1
    return res
def part2(positions):
    p1_pos, p2_pos = positions
    #        p1_pos, p2_pos, p1_score, p2_score, next_player, universe_count
    game_queue = deque([(p1_pos, p2_pos,0,0,1,1)])
    dirac = gen_dirac_dict(3)
    wins = {1:0,2:0}
    while len(game_queue) > 0:
        p1_pos,p2_pos,p1_score,p2_score,next_player,universe_count = game_queue.popleft()
        for roll, universe_multiplier in dirac.items():
            n_universe_count = universe_count * universe_multiplier
            if next_player == 1:
               n_p1_pos = ((p1_pos + roll - 1)  % 10 ) + 1
               n_p1_score = p1_score + n_p1_pos
               if n_p1_score >= 21:
                   wins[1] += n_universe_count
               else:
                   game_queue.append((n_p1_pos,p2_pos,n_p1_score,p2_score,2,n_universe_count))
            else:
               n_p2_pos = ((p2_pos + roll - 1)  % 10 ) + 1
               n_p2_score = p2_score + n_p2_pos
               if n_p2_score >= 21:
                   wins[2] += n_universe_count
               else:
                   game_queue.append((p1_pos,n_p2_pos,p1_score,n_p2_score,1,n_universe_count))
    return wins[1] if wins[1] > wins[2] else wins[2]

def parse(lines):
    p1 = int(lines[0].split(':')[1])
    p2 = int(lines[1].split(':')[1])
    return(p1,p2)
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
    if p1 == 739785:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 444356092776315:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
