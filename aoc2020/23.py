#!/usr/bin/env python3

import sys
from collections import OrderedDict
# import re
from tqdm import tqdm
import numpy as np
from numba import njit, deferred_type, int64, optional
from numba.experimental import jitclass
from dataclasses import dataclass, field
# from functools import cache,lru_cache

@dataclass
class Cups:
    cups : list[int] = field(default_factory=list)
    def ix(self, c: int) -> int:
        return self.cups.index(c)

    def __getitem__(self, val):
        return self.cups[val]

    def pop(self, p: int) -> int:
        if p >= len(self.cups):
            i = 0
        else:
            i = p + 1
            i = i % len(self.cups)
        ret = self.cups[i]
        self.cups = self.cups[0:i] + self.cups[i + 1:]
        return ret
    def push(self, p: int, c:int):
        if p >= len(self.cups):
            p = p % len(self.cups)
        self.cups = self.cups[0:p + 1] + [c] + self.cups[p + 1:]
    def print(self, current: int, p):
        s =  ""
        for i, c in enumerate(self.cups):
            if i == current:
                s += f"({c}) "
            else:
                s += f"{c} "
        p("cups:  " + s)
    def reindex(self,old: int, new: int):
        diff = new - old
        diff = diff % len(self.cups)
        self.cups = self.cups[diff:] + self.cups[:diff]
    def min(self):
        return min(self.cups)
    def max(self):
        return max(self.cups)
    def __len__(self):
        return len(self.cups)

def dbg(s):
    pass
def oldpart1(cups):
    p = print
    cups = Cups(cups)
    minc = cups.min()
    maxc = cups.max()
    current = 0
    for move in range(100):
        if move > 9:
            p = dbg
        p(f"-- move {move + 1} --")
        destination = cups[current] - 1
        cval = cups[current]
        cups.print(current,p)
        pick_up = [cups.pop(current), cups.pop(current), cups.pop(current)]
        p(f"pick up: {', '.join([str(x) for x in pick_up])}")
        if destination < minc:
            destination = maxc
        while destination in pick_up:
            destination -= 1
            if destination < minc:
                destination = maxc
        p(f"destination: {destination}")
        didx = cups.ix(destination)
        p(f"destination index: {didx}")
        cups.print(current,p)
        for i, c in enumerate(pick_up):
            cups.push(didx + i, c)
        cups.reindex(current, cups.ix(cval))
        cups.print(current, p)
        current += 1
        if current == len(cups):
            current = 0
    one = cups.ix(1)
    s = ""
    for i in range(len(cups) - 1):
        s += str(cups.pop(one))
    return s

def ringpart1(cups):
    cupsr = CupsRing(cups)
    for _ in tqdm(range(100)):
        cupsr.move()
    one = cupsr.ix(1) + 1
    s = ""
    for i in range(cupsr.length - 1):
        ix = (one + i) % cupsr.length
        s += str(cupsr.cups[ix])
    return s

def llpart1(cups):
    cn = create_linked_list(cups)
    m = max(cups)
    for _ in tqdm(range(100)):
        cn = move(cn,m)
    one = cn.find(1)
    s = ""
    for i in range(len(cups) - 1):
        cn = cn.next
        s += str(cn.data)
    return s
def part1(cups):
    return "".join(map(str,iter_next_cups(nbsolve(np.array(cups), 100))))[1:]
@dataclass
class CupsRing:
    cups : list[int] = field(default_factory=list)
    pos: int = 0
    length: int = 0
    max: int = 0
    def __post_init__(self):
        self.length = len(self.cups)
        self.max = max(self.cups)
    def current_cup_label(self) -> int:
        return self.cups[self.pos]
    def take_cups(self) -> list[int]:
        if self.pos + 4 <= self.length:
            t = self.cups[self.pos + 1: self.pos + 4]
            self.cups = self.cups[:self.pos + 1] + self.cups[self.pos + 4:]
        else:
            t = self.cups[self.pos + 1:] + self.cups[:4 - self.length + self.pos]
            self.cups = self.cups[4 - self.length + self.pos : self.pos + 1]
            self.pos = self.length - 4
        return t
    def put_cups(self, after:int, cups: list[int]):
        self.cups = self.cups[:after + 1] + cups + self.cups[after + 1:]
        if after < self.pos:
            self.pos += 3
    def ix(self, c: int) -> int:
        return self.cups.index(c)
    def move(self):
        t = self.take_cups()
        dl = self.current_cup_label() - 1
        if dl == 0:
            dl = self.max
        while dl in t:
            dl = dl - 1
            if dl == 0:
                dl = self.max
        d = self.cups.index(dl)
        self.put_cups(d,t)
        self.pos = (self.pos + 1) % self.length

cupsnode_t = deferred_type()
cupsnode_spec = OrderedDict()
cupsnode_spec['data'] = int64
cupsnode_spec['next'] = optional(cupsnode_t)

#@jitclass(cupsnode_spec)
class CupsNode:
    def __init__(self,c: int, next_cup:'CupsNode'):
        self.data = c
        self.next = next_cup
    def to_list(self) -> list[int]:
        l = [self.data]
        n = self.next
        while n is not self and n is not None:
            l.append(n.data)
            n = n.next
        return l
    def take_3_cups(self: 'CupsNode') -> 'CupsNode':
        new_next = self.next.next.next.next
        ret = self.next
        self.next = new_next
        return ret
    def find(self,c : int,s: int = 1_000_000) -> 'CupsNode':
        if self.data == c:
            return self
        n = self.next
        i = 1
        while i <=s and n is not self and n.data != c:
            n = n.next
            i += 1
        if n is not None and n.data == c:
            return n
    def __str__(self):
        return str(self.data)

#cupsnode_t.define(CupsNode.class_type.instance_type)

def create_linked_list(cups: list[int]) -> CupsNode:
    tail = CupsNode(cups[-1], None)
    p = tail
    for c in cups[-2:0:-1]:
        p = CupsNode(c, p)
    p =  CupsNode(cups[0], p)
    tail.next = p
    return p

#@njit((cupsnode_t,cupsnode_t))
def insert_after(n: 'CupsNode', cn: 'CupsNode'):
    cn.next.next.next = n.next
    n.next = cn

#@njit
def move(c: CupsNode, m: int) -> CupsNode:
    t = c.take_3_cups()
    dl = c.data - 1
    if dl == 0:
        dl = m
    while t.find(dl,2):
        dl -= 1
        if dl == 0:
            dl = m
    dn = c.find(dl)
    insert_after(dn,t)
    return c.next

@njit
def nbmove(current, next_cups):
    a = next_cups[current]
    b = next_cups[a]
    c = next_cups[b] # take three after current
    after = next_cups[c]

    d = current
    while(d := d - 1) in (a,b,c) or d == 0:
        if d == 0:
            d = len(next_cups) # equivalent to max

    next_cups[current] = after
    next_cups[c] = next_cups[d]
    next_cups[d] = a
    return after

@njit
def nbsolve(cups, moves):
    next_cups = np.zeros(len(cups) + 1, dtype=np.uint32)
    for f, t in zip(cups, cups[1:]):
        next_cups[f] = t # map to index of next valued cup
    next_cups[cups[-1]] = cups[0] # make circular

    current = cups[0]
    for _ in range(moves):
        current = nbmove(current, next_cups)
    return next_cups

def iter_next_cups(next_cups):
    current = 1
    yield current
    while (current := next_cups[current]) != 1:
        yield current

def part2(cups):
    ca = np.array(cups + list(range(len(cups) + 1, 1_000_001)))
    res = nbsolve(ca, 10_000_000)
    return int(res[1]) * int(res[res[1]])


def llpart2(cups):
    cups.extend(range(max(cups) + 1,1_000_001))
    cn = create_linked_list(cups)
    for _ in tqdm(range(10_000_000)):
        cn = move(cn, 1_000_000)
    one = cn.find(1)
    return one.next.data * one.next.next.data

def oldpart2(cups):
    cups.extend(range(max(cups) + 1,1_000_001))
    cupsr = CupsRing(cups)
    for _ in tqdm(range(10_000_000)):
        cupsr.move()
    l = cupsr.ix(1)
    return cupsr.cups[l + 1] * cupsr.cups[l + 2]

def parse(lines):
    return [int(c) for c in lines[0]]

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
    if p1 == "67384529":
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 149245887792:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
