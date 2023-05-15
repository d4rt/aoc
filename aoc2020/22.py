#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
from functools import cache,lru_cache
from copy import deepcopy
from itertools import islice

def part1(decks):
    p1, p2 = decks
    p1 = deque(p1)
    p2 = deque(p2)
    r = 0
    while len(p1) > 0 and len(p2) > 0:
        r += 1
        print(f"""-- Round {r} --
        Player 1's deck: {p1}
        Player 2's deck: {p2}""")
        p1c = p1.popleft()
        p2c = p2.popleft()
        print(f"""Player 1 plays: {p1c}
        Player 2 plays: {p2c}""")
        if p1c > p2c:
            print(f"Player 1 wins the round")
            p1.append(p1c)
            p1.append(p2c)
            win = p1
        else:
            print(f"Player 2 wins the round")
            p2.append(p2c)
            p2.append(p1c)
            win = p2
    score = 0
    mul = len(win)
    print(mul)
    print(win)
    for card in win:
        print(f"{card} * {mul}")
        score += card * mul
        mul -= 1
    return score
def recursive_combat(p1,p2,gn):
    seen = set()
    r = 0
    seen.add((tuple(p1),tuple(p2)))
    print(f"=== Game {gn} ===")
    print()
    ng = gn + 1
    while len(p1) > 0 and len(p2) > 0:
        r += 1
        print(f"""-- Round {r} (Game {gn}) --
Player 1's deck: {p1}
Player 2's deck: {p2}""")
        p1c = p1.popleft()
        p2c = p2.popleft()
        print(f"""Player 1 plays: {p1c}
Player 2 plays: {p2c}""")
        if len(p1) >= p1c and len(p2) >= p2c:
            print("Playing a sub-game to determine the winner...")
            print()
            winner, _, _, ng = recursive_combat(deque(islice(p1,0,p1c)),deque(islice(p2,0,p2c)),ng)
            print(f"... anyway, back to game {gn}")
        elif p1c > p2c:
            winner = 1
        else:
            winner = 2
        if winner == 1:
            print(f"Player 1 wins round {r} of game {gn}!")
            print()
            p1.append(p1c)
            p1.append(p2c)
        else:
            print(f"Player 2 wins round {r} of game {gn}")
            print()
            p2.append(p2c)
            p2.append(p1c)
        if (tuple(p1),tuple(p2)) in seen:
            print(f"Seen {p1}, {p2} before, player 1 wins")
            return 1, p1, p2, ng
        seen.add((tuple(p1),tuple(p2)))
    return winner, p1, p2, ng

def part2(decks):
    p1, p2 = decks
    winner, p1, p2, ng = recursive_combat(deque(p1),deque(p2),1)
    if winner == 1:
        win = p1
    else:
        win = p2
    score = 0
    mul = len(win)
    print(mul)
    print(win)
    for card in win:
        print(f"{card} * {mul}")
        score += card * mul
        mul -= 1
    return score


def parse(data):
    p1,p2 = data.split('\n\n')
    p1 = [int(x) for x in p1.split('\n')[1:]]
    p2 = [int(x) for x in p2.split('\n')[1:]]
    return (p1, p2)


if __name__ == '__main__':
    test_infile = sys.argv[0][:-3] + '-test.txt'
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split('\n')]
    test_parsed  = parse(test_data)

    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    lines = [x for x in data.split('\n')]
    parsed  = parse(data)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 306:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 291:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
