#!/usr/bin/env python3

import sys
from collections import defaultdict
# import re
# from tqdm import tqdm
import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from typing import Iterator

def edge_scores(edge: np.ndarray) -> list[int]:
    # https://stackoverflow.com/questions/67270228/how-to-change-a-binary-numpy-array-into-an-int
    e = ''.join(edge.astype(str).tolist())
    return [int(e, 2),int(e[::-1],2)]

def tile_edge_score(tile: np.ndarray) -> list[int]:
    """Given a tile  (2d binary array) convert the edges to 'scores' (ie. ints)
       Tiles can be rotated or flipped, so we also reverse each edge to account for flips"""
    top = tile[0, :]
    bottom = tile[-1, :]
    left = tile[:, 0].T
    right = tile[:, -1].T
    scores = []
    for edge in [top,bottom,left,right]:
        scores.extend(edge_scores(edge))
    return scores

def rotate_tile(tile : np.ndarray) -> Iterator[np.ndarray]:
    tiles = []
    for r in range(4):
        tile = tile.copy()
        tile = np.rot90(tile)
        yield tile
        yield np.fliplr(tile)
        yield np.flipud(tile)
        yield np.fliplr(np.flipud(tile))


def part1(tiles):
    # calculate tile adjacency score 
    edges = {tile: tile_edge_score(tiles[tile]) for tile in tiles}
    # find corners using uncommon values
    edge_frequency = defaultdict(int)
    edge_to_tile = defaultdict(int)

    for tile in tiles:
        for edge_score in edges[tile]:
            edge_frequency[edge_score] += 1
            edge_to_tile[edge_score] = tile
    corner_candidates = set()  # use a set - each tile will have two unique edges
    for tile in tiles:
        scores = [edge_frequency[score] for score in edges[tile]]
        if scores.count(1) == 4: # 2 edges, 2 scores per edge (accounting for flipping)
            corner_candidates.add(tile)

    # for this part we don't actually have to tile it, just score the corners
    assert len(corner_candidates) == 4 # is our solution unique?
    p1 = 1
    for tile in corner_candidates:
        p1  *= tile
    return p1

def part2(tiles):
    # Find the corners as in part 1
    # calculate tile adjacency score
    edges = {tile: tile_edge_score(tiles[tile]) for tile in tiles}
    # find corners using uncommon values
    edge_frequency = defaultdict(int)
    edge_to_tile = defaultdict(list)

    for tile in tiles:
        for edge_score in edges[tile]:
            edge_frequency[edge_score] += 1
            edge_to_tile[edge_score].append(tile)
    corner_candidates = set()  # use a set - each tile will have two unique edges
    for tile in tiles:
        scores = [edge_frequency[score] for score in edges[tile]]
        if scores.count(1) == 4: # 2 edges, 2 scores per edge (accounting for flipping)
            corner_candidates.add(tile)

    # tile - find the orientation of all pieces
    # pick any of the corners
    top_left = list(corner_candidates)[0]
    tiling_ids = [[top_left]]
    available_tiles = set(tiles) - {top_left}
    candidates = set()
    for edge in edges[top_left]:
        for tile in edge_to_tile[edge]:
            if tile != top_left:
                candidates.add(tile)
    available_tiles -= candidates
    candidates = list(candidates)
    assert len(candidates) == 2
    left_tile = candidates[0]
    bottom_tile = candidates[1]
    # special case - (L) the first tile along also helps us decide the orientation
    # special case - (B) we also want to find the tile beneath to help decide the orientation
    #
    # TL L
    # B
    m = False
    for tl in rotate_tile(tiles[top_left]):
        for l in rotate_tile(tiles[left_tile]):
            for b in rotate_tile(tiles[bottom_tile]):
                if np.all(tl[-1,:] == b[0,:]) and np.all(tl[:, -1] == l[:,0]):
                    m = True
                    break
            if m:
                break
        if m:
            break
    assert m
    tiling = [[tl,l],[b]]

    j = 0 # current row
    i = 2 # current col
    while len(available_tiles) > 0:
        # find a matching tile
        # next row until same length as first row
        if j == 0:
            edge = int(''.join(tiling[j][i - 1][:,-1].astype(str).tolist()),2)
            candidates = set(edge_to_tile[edge]) & available_tiles
            assert len(candidates) == 1
            tile = list(candidates)[0]
            m = False
            for t in rotate_tile(tiles[tile]):
                if np.all(tiling[j][i - 1][:, -1] == t[:,0]):
                    m = True
                    break
            assert m
            tiling[j].append(t)
            available_tiles -= {tile}
            if tile in corner_candidates:
                width = i
                j = 1
                i = 1
            else:
                i += 1
        else:
            edge_top = int(''.join(tiling[j - 1][i][-1,:].astype(str).tolist()),2)
            if i == 0:
                candidates = set(edge_to_tile[edge_top]) & available_tiles
            else:
                edge_left = int(''.join(tiling[j][i - 1][:,-1].astype(str).tolist()),2)
                candidates = set(edge_to_tile[edge_left]) & set(edge_to_tile[edge_top]) & available_tiles
            assert len(candidates) == 1
            tile = list(candidates)[0]
            m = False
            for t in rotate_tile(tiles[tile]):
                if i == 0:
                    if np.all(tiling[j - 1][i][-1,:] == t[0,:]):
                        m = True
                        break
                elif np.all(tiling[j][i - 1][:,-1] == t[:,0]) and np.all(tiling[j - 1][i][-1,:] == t[0,:]):
                    m = True
                    break
            assert m
            if i == 0:
                tiling.append([t])
            else:
                tiling[j].append(t)
            available_tiles -= {tile}
            if i == width:
                j += 1
                i = 0
            else:
                i = i + 1
    # build array image
    width = width + 1
    height = j
    tile_height, tile_width = np.shape(tiles[top_left])
    tile_height = tile_height - 2
    tile_width = tile_width - 2
    image = np.zeros(((height * tile_height), (width * tile_width)))

    for j, r in enumerate(tiling):
        for i, t in enumerate(r):
            image[j * tile_height : (j + 1) * tile_height, i * tile_width : (i + 1) * tile_width] = t[1:-1,1:-1] # slice off the first and last row/col

    # search for nessie
    nessie_text = """..................#.
#....##....##....###
.#..#..#..#..#..#..."""
    nessie = np.array([[d[x] for x in line ] for line in nessie_text.split('\n') ],dtype=int)
    nessie_shape = np.shape(nessie)
    print_image(nessie)
    m = False
    for image in rotate_tile(image):
        wv = np.lib.stride_tricks.sliding_window_view(image, nessie_shape, writeable=True)
        for vv in wv:
            for v in vv:
                if np.all(v[nessie == 1] == 1):
                    v[nessie == 1] = 0
                    m = True
        if m:
            return np.count_nonzero(image)

d = {'.': 0, '#': 1}
p = {0 : '.', 1: '#'}
def print_image(image: np.ndarray):
    for row in image:
        print(''.join([p[x] for x in row]))
def print_tiling(tiling: list[list[np.ndarray]]):
    for row in tiling:
        for i in range(len(row[0])):
            r = ''
            for tile in row:
                r += ''.join([p[x] for x in tile[i]])
            print(r)
def parse(data):
    tiles = data.split('\n\n')
    tile_arrays = {}
    for tile in tiles:
        tile = tile.split('\n')
        tile_id = int(tile[0].split(' ')[1][:-1])
        tile_a = np.array([[d[x] for x in line] for line in tile[1:]],dtype=int)
        tile_arrays[tile_id] = tile_a
    return tile_arrays

if __name__ == '__main__':
    test_infile = sys.argv[0][:-3] + '-test.txt'
    test_data = open(test_infile).read().strip()
    test_parsed  = parse(test_data)

    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    parsed  = parse(data)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 20899048083289:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 273:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
