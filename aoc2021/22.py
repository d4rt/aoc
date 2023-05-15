#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
import re
from tqdm import tqdm
# import numpy as np
from dataclasses import dataclass, field
# from functools import cache,lru_cache
import pytest
def dbg(str):
    pass
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

    def __lt__(self,p: 'Point') -> bool:
        return self.x < p.x and self.y < p.y and self.z < p.z

    def __gt__(self,p: 'Point') -> bool:
        return self.x > p.x and self.y > p.y and self.z > p.z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

@dataclass(frozen=True)
class Cuboid:
    origin: Point
    maximum: Point
    def size(self):
        assert self.maximum.x >= self.origin.x
        assert self.maximum.y >= self.origin.y
        assert self.maximum.z >= self.origin.z
        xs = (self.maximum.x - self.origin.x) + 1
        ys = (self.maximum.y - self.origin.y) + 1
        zs = (self.maximum.z - self.origin.z) + 1
        return xs*ys*zs
    def __iter__(self):
        for x in range(self.origin.x,self.maximum.x + 1):
            for y in range(self.origin.y,self.maximum.y + 1):
                for z in range(self.origin.z,self.maximum.z + 1):
                    yield Point(x,y,z)
    def __contains__(self,p: Point) -> bool:
        return (self.origin.x <= p.x <= self.maximum.x and
                self.origin.y <= p.y <= self.maximum.y and
                self.origin.z <= p.z <= self.maximum.z)
    def __sub__(self,c:'Cuboid') -> list['Cuboid']:
        if (self.origin.x > c.maximum.x or
            self.origin.y > c.maximum.y or
            self.origin.z > c.maximum.z):
            return [self]# no intersection
        if (self.maximum.x < c.origin.x or
            self.maximum.y < c.origin.y or
            self.maximum.z < c.origin.z):
            return [self]# no intersection
        #
        if (c.origin.x <= self.origin.x  and self.maximum.x <= c.maximum.x and
            c.origin.y <= self.origin.y  and self.maximum.y <= c.maximum.y and
            c.origin.z <= self.origin.z  and self.maximum.z <= c.maximum.z):
            return [] # c is bigger than us, so nothing
        pieces = []
        dbg(self)
        dbg(c)
        # the x origin is inside our cube, so slice it by x
        #dbg(f"self.origin.x {self.origin.x}, c.origin.x {c.origin.x}")
        if self.origin.x < c.origin.x:
            # above slice
            piece = Cuboid(self.origin,Point(c.origin.x - 1,self.maximum.y,self.maximum.z)) # top slice
            dbg(f"x above = {piece}")
            if piece.size() != 0:
                pieces.append(piece)
        #dbg(f"self.maximum.x {self.maximum.x}, c.maximum.x {c.maximum.x}")
        if c.maximum.x < self.maximum.x:
            # below slice
            piece = Cuboid(Point(c.maximum.x + 1,self.origin.y, self.origin.z),self.maximum)
            dbg(f"x below = {piece}")
            if piece.size() != 0:
                pieces.append(piece)
        # middle piece(s)
        #
        #   y
        # +-------------+ self.origin.z
        # |  1 | 2  | 3 |
        # +----+----+---+ c.origin.z
        #z|  4 |  C | 5 |
        # |    |    |   |
        # +----+----+---+ c.maximum.z
        # |  6 |  7 | 8 |
        # +----+----+---+ self.maximum.z
        #      c
        #      origin
        #      y
        #           c
        #           maximum
        #           y
        # 1
        ox = max(self.origin.x,c.origin.x) # c if contained, but if c starts 'above' us we want to start from our x (no top slice)
        mx = min(c.maximum.x,self.maximum.x) # similarly c if contained but ours if it ends 'below' us
        if ox <= mx:
            oz = max(self.origin.z,c.origin.z)
            mz = min(self.maximum.z,c.maximum.z)
            dbg(f"mx,ox {mx},{ox} ")
            # do 1,2,3 exist?
            dbg(f"self.origin.z {self.origin.z}, c.origin.z {c.origin.z}")
            if self.origin.z < c.origin.z:
                piece = Cuboid(Point(ox,self.origin.y,self.origin.z),Point(mx,self.maximum.y,c.origin.z - 1))
                dbg(f"123 piece {piece}")
                if piece.size() != 0:
                    pieces.append(piece)
            # does 4 exist?
            if self.origin.y < c.origin.y:
                piece = Cuboid(Point(ox,self.origin.y,oz),Point(mx,c.origin.y - 1,mz))
                dbg(f"4 piece {piece}")
                if piece.size() != 0:
                    pieces.append(piece)
            # does 5 exist?
            if c.maximum.y < self.maximum.y:
                piece = Cuboid(Point(ox,c.maximum.y + 1,oz),Point(mx,self.maximum.y,mz))
                dbg(f"5 piece {piece}")
                if piece.size() != 0:
                    pieces.append(piece)
            # do 6,7,8 exist
            if c.maximum.z < self.maximum.z:
                piece = Cuboid(Point(ox,self.origin.y,c.maximum.z + 1),Point(mx,self.maximum.y,self.maximum.z))
                dbg(f"678 piece {piece}")
                if piece.size() != 0:
                    pieces.append(piece)
        return pieces


    @classmethod
    def from_ins(cls,xf:int, xt:int,yf:int,yt:int,zf:int,zt:int) -> 'Cuboid':
       min_x = min(xf,xt)
       max_x = max(xf,xt)
       min_y = min(yf,yt)
       max_y = max(yf,yt)
       min_z = min(zf,zt)
       max_z = max(zf,zt)
       return Cuboid(Point(min_x,min_y,min_z),Point(max_x,max_y,max_z))

def apply_instruction(i: dict, cuboids: list[Cuboid]) -> list[Cuboid]:
    c = Cuboid.from_ins(i['xf'],i['xt'],i['yf'],i['yt'],i['zf'],i['zt'])
    new_cuboids = []
    for o in cuboids:
        new_cuboids.extend(o - c)
    if i['op'] == 'on':
        new_cuboids.append(c)
    return new_cuboids

def size(cuboids: list[Cuboid]):
    return sum([c.size() for c in cuboids])

def contains(cuboids: list[Cuboid], p: Point):
    return any([p in c for c in cuboids])

def part1(instructions):
    cuboids = []
    for i in tqdm(instructions):
        cuboids = apply_instruction(i,cuboids)
    ins = {'op':'off','xf':-50,'xt':50,'yf':-50,'yt':50,'zf':-50,'zt':50}
    initialisation_cuboids = apply_instruction(ins, cuboids)
    return size(cuboids) - size(initialisation_cuboids)

def part2(instructions):
    cuboids = []
    for i in tqdm(instructions):
        cuboids = apply_instruction(i,cuboids)
    return size(cuboids)

def parse(lines):
    re_i = re.compile(r"(?P<op>on|off) x=(?P<xf>[-0-9]+)\.\.(?P<xt>[-0-9]+),y=(?P<yf>[-0-9]+)\.\.(?P<yt>[-0-9]+),z=(?P<zf>[-0-9]+)\.\.(?P<zt>[-0-9]+)")
    instructions = []
    for line in lines:
        match = re_i.match(line)
        if match:
            d = match.groupdict()
            d['xf'] = int(d['xf'])
            d['xt'] = int(d['xt'])
            d['yf'] = int(d['yf'])
            d['yt'] = int(d['yt'])
            d['zf'] = int(d['zf'])
            d['zt'] = int(d['zt'])
            instructions.append(d)
    return instructions

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
    if p1 == 590784:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 39769202357779:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

def test_single_cuboid():
    lines = ['on x=10..12,y=10..12,z=10..12']
    cuboids = []
    cuboids = apply_instruction(parse(lines)[0],cuboids)
    assert size(cuboids) == 27

def test_remove_single_cube():
    lines = ['on x=10..12,y=10..12,z=10..12']
    cuboids = apply_instruction(parse(lines)[0],[])
    s = size(cuboids)
    for x in range(10,13):
        for y in range(10,13):
            for z in range(10,13):
                new_cuboids = apply_instruction({'op':'off','xf':x,'xt':x,'yf':y,'yt':y,'zf':z,'zt':z},cuboids)
                if size(new_cuboids) != s - 1:
                    print(new_cuboids)
                    assert size(new_cuboids) == s - 1
                else:
                    print(f"success {x},{y},{z}")

def test_remove_block_on_corner():
    lines = ['on x=10..12,y=10..12,z=10..12']
    cuboids = apply_instruction(parse(lines)[0],[])
    s = size(cuboids)
    new_cuboids = apply_instruction({'op': 'off', 'xf': -1, 'xt':10, 'yf': 9,'yt': 10, 'zf':10,'zt':11}, cuboids) # removes 2 blocks
    assert size(new_cuboids) == s - 2

def test_remove_alternative_corners():
    lines = ['on x=10..12,y=10..12,z=10..12']
    cuboids = apply_instruction(parse(lines)[0],[])
    s = size(cuboids)
    new_cuboids = apply_instruction({'op': 'off', 'xf': -1, 'xt':10, 'yf': 9,'yt': 10, 'zf':10,'zt':11}, cuboids) # removes 2 blocks
    new_cuboids = apply_instruction({'op': 'off', 'xf': 12, 'xt':12, 'yf': 9,'yt': 10, 'zf':10,'zt':11}, new_cuboids) # removes 2 blocks
    assert size(new_cuboids) == s - 4

def test_overlapping_on():
    lines = ['on x=10..12,y=10..12,z=10..12','on x=11..13,y=11..13,z=11..13']
    instructions = parse(lines)
    cuboids = []
    for i in instructions:
        cuboids = apply_instruction(i,cuboids)
    print(cuboids)
    assert size(cuboids) == 27 + 19


def test_reboot():
    lines = ['on x=10..12,y=10..12,z=10..12',
             'on x=11..13,y=11..13,z=11..13',
             'off x=9..11,y=9..11,z=9..11',
             'on x=10..10,y=10..10,z=10..10']
    totals = [27,27+19,(27+19)-8,((27+19)-8)+1]
    instructions = parse(lines)
    cuboids = []
    points = set()
    for i, t in zip(instructions,totals):
        print(i)
        cuboids = apply_instruction(i,cuboids)
        new_points = set([p for cube in cuboids for p in cube])
        if i['op'] == 'on':
            print("added points")
            print(new_points - points)
        else:
            print("removed points")
            print(points - new_points)
            print("added points")
            print(new_points - points)
        print(f"cuboids {cuboids}, size {size(cuboids)} , total {t}")
        points = new_points
        assert size(cuboids) == t
