#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from operator import add
def flip(s:set ,t:tuple):
    """utility function, if in the set, remove, if not, add"""
    if t in s:
        s.remove(t)
    else:
        s.add(t)

def part1(black:set) -> int:
    return len(black)
# https://www.redblobgames.com/grids/hexagons/#neighbors-axial
directions = {'e': (1,0),
                'se': (0,1),
                'sw': (-1,1),
                'w': (-1,0),
                'nw':(0, -1),
                'ne':(1,-1)}

def adj(tile: tuple) -> list[tuple]:
    return [tuple(map(add,tile,d)) for d in directions.values()]

def tiles_conway(black: set) -> set:
    # for each tile, add one to all adjacent tiles
    adjacencies = defaultdict(int)
    for tile in black:
        for a in adj(tile):
            adjacencies[a] += 1

    return { tile for tile in adjacencies if (adjacencies[tile] == 2 and tile not in black) or (tile in black and (adjacencies[tile] == 1 or adjacencies[tile] == 2)) }

def part2(black:set) -> int:
    for _ in range(100):
        black = tiles_conway(black)
    return len(black)

def parse_line(l:str) -> list[str]:
    dirs = ['e','se','sw','w','nw','ne']
    directions = []
    while len(l) > 0:
        for d in dirs:
            if l.startswith(d):
                directions.append(d)
                l = l[len(d):]
    return directions

def parse(lines: list[str]) -> set:
    tile_directions = [parse_line(line) for line in lines]
    # modelling using https://www.redblobgames.com/grids/hexagons/
    # axial q r
    black = set()
    for tile_direction in tile_directions:
        location = (0,0)
        for step in tile_direction:
            location = tuple(map(add,location, directions[step]))
        flip(black, location)
    return black

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
    if p1 == 10:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 2208:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

def test_adj():
    l = (0,0)
    a = adj(l)
    print(a)
    assert len(a) == 6
    assert false
