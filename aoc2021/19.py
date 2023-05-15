#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np
from dataclasses import dataclass, field
import pytest

@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0
    z: int = 0
    @classmethod
    def from_string(cls,s: str) -> 'Point':
        xyz = s.split(",")
        return cls(x=int(xyz[0]), y=int(xyz[1]), z=int(xyz[2]))

    @classmethod
    def from_tuple(cls,t: tuple) -> 'Point':
        return cls(t[0],t[1],t[2])

    def __sub__(self,p: 'Point') -> 'Point':
        return Point(self.x-p.x, self.y-p.y, self.z-p.z)

    def __add__(self,p: 'Point') -> 'Point':
        return Point(self.x+p.x, self.y+p.y, self.z+p.z)

    def abs_distance(self,p: 'Point') -> int:
        return abs(self.x - p.x) + abs(self.y - p.y) + abs(self.z - p.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z



@dataclass
class Orientation:
    facings: list[int] = field(default_factory= lambda: [1,1,1]) # 3 lots of  1, -1
    mapping: dict = field(default_factory= lambda: {0: 0, 1: 1, 2:2}) # relative to scanner 0
    origin: Point = Point(0,0,0) # relative to scanner 0
    def canonicalise(self,p: Point) -> Point:
        # unpack point into a tuple, so we can use indexing instead of if statements
        tp = tuple(p)
        # mapping then facing then translate to origin
        x = tp[self.mapping[0]] * self.facings[0] + self.origin.x
        y = tp[self.mapping[1]] * self.facings[1] + self.origin.y
        z = tp[self.mapping[2]] * self.facings[2] + self.origin.z
        return Point(x,y,z)

@dataclass
class Scanner:
    number: int = 0
    beacons: list[Point] = field(default_factory=list) # relative to self
    location: Point = None # starts unknown
    orientation: Orientation = None # starts unknown
    def canonicalise(self):
        self.beacons = [self.orientation.canonicalise(p) for p in self.beacons]

def find_common(s1: Scanner, s2: Scanner):
    orig_s2 = s2.beacons.copy()
    s1_dists = np.zeros((len(s1.beacons),len(s1.beacons)), dtype=int)
    for i, x in enumerate(s1.beacons):
        for j, y in enumerate(s1.beacons):
            s1_dists[i][j] = x.abs_distance(y)
    s2_dists = np.zeros((len(s2.beacons),len(s2.beacons)), dtype=int)
    for i, x in enumerate(s2.beacons):
        for j, y in enumerate(s2.beacons):
            s2_dists[i][j] = x.abs_distance(y)
    for j, c in enumerate(s1_dists):
        for i, r in enumerate(s2_dists):
            match_count = np.count_nonzero(np.isin(c,r))
            if match_count >= 12:
                # build mapping dict
                s1_to_s2 = {}
                s2_to_s1 = {}
                for k, d in enumerate(c):
                    w = np.where(r==d)
                    if len(w[0]) == 1:
                        s1_to_s2[k] = w[0][0]
                        s2_to_s1[w[0][0]] = k
                # calculate position and orientation of scanner using common points
                # can figure out permutations of x,y,z with comparing abs distances pairwise
                # also orientation by seeing if same or inverse
                items = list(s1_to_s2.items())
                s1_dist = s1.beacons[items[0][0]] - s1.beacons[items[1][0]]
                s2_dist = s2.beacons[items[0][1]] - s2.beacons[items[1][1]]
                s2_orientation = Orientation()
                for k, m in enumerate(s1_dist):
                    if m == s2_dist.x: # x is 0
                        s2_orientation.mapping[k] = 0
                        s2_orientation.facings[k] = 1
                        continue
                    if m == - s2_dist.x:
                        s2_orientation.mapping[k] = 0
                        s2_orientation.facings[k] = -1
                        continue
                    if m == s2_dist.y: # y is 1
                        s2_orientation.mapping[k] = 1
                        s2_orientation.facings[k] = 1
                        continue
                    if m == - s2_dist.y:
                        s2_orientation.mapping[k] = 1
                        s2_orientation.facings[k] = -1
                        continue
                    if m == s2_dist.z: # z is 2
                        s2_orientation.mapping[k] = 2
                        s2_orientation.facings[k] = 1
                        continue
                    if m == - s2_dist.z:
                        s2_orientation.mapping[k] = 2
                        s2_orientation.facings[k] = -1
                        continue
                b2 = s2_orientation.canonicalise(s2.beacons[items[0][1]])
                s2_orientation.origin = s1.beacons[items[0][0]] - b2
                s2.orientation = s2_orientation
                s2.location = s2_orientation.origin
                s2.canonicalise()
                return True


def part1(scanners):
    # problem spec says we have at least 12 overlapping beacons
    # for some pair of scanners
    s0 = scanners[0]
    canonicalised = [0]
    to_go = list(range(len(scanners)))
    del to_go[0]
    for i, s in enumerate(scanners):
        if i == 0:
            continue
        if find_common(s0,s):
            canonicalised.append(i)
            to_go.remove(i)
    while len(to_go) > 0:
        for i, s in enumerate(scanners):
            if i in canonicalised:
                continue
            for j in canonicalised:
                if find_common(scanners[j], scanners[i]):
                    to_go.remove(i)
                    canonicalised.append(i)
                    break
    beacons = set()
    for s in scanners:
        beacons.update(s.beacons)
    return(len(beacons))


def part2(scanners):
    distances = [s1.location.abs_distance(s2.location) for s1 in scanners for s2 in scanners]
    return max(distances)

def parse(data):
    scans = [x.split('\n') for x in  data.split('\n\n')]
    scanners = [Scanner(i,[Point.from_string(s) for s in scanner[1:]]) for i, scanner in enumerate(scans)]
    scanners[0].orientation = Orientation()
    scanners[0].location = Point(0,0,0)
    return scanners

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
    if p1 == 79:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 3621:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

@pytest.fixture
def test_parse():
    test_infile = '19-test.txt'
    test_data = open(test_infile).read().strip()
    test_parsed  = parse(test_data)
    return test_parsed

def test_find_common_beacons(test_parse):
    s1 = test_parse[0]
    s2 = test_parse[1]
    find_common(s1,s2)
    assert s2.location == Point(68,-1246,-43)
