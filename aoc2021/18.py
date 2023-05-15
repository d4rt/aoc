#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
from dataclasses import dataclass, field, asdict
import pytest
import json

@dataclass
class Node:
    l : 'Node' = None
    r : 'Node' = None
    v : int = None
    depth: int = 0

    @classmethod
    def from_string(cls, str : str) -> 'Node':
        j = json.loads(str)
        return cls.from_list(j)
    @classmethod
    def from_list(cls, l : list, depth : int = 0) -> 'Node':
        node = cls()
        if type(l[0]) is int:
            node.l = cls(v=l[0],depth=depth)
        else:
            node.l = cls.from_list(l[0],depth + 1)
        if type(l[1]) is int:
            node.r = cls(v=l[1],depth=depth)
        else:
            node.r = cls.from_list(l[1],depth + 1)
        return node

    def __iter__(self):
        # only iterate over the value nodes (useful for the reduce later)
        if self.v is not None:
            yield self
        else:
            for node in self.l:
                yield node
            for node in self.r:
                yield node

    def __str__(self):
        if self.v is not None:
            return str(self.v)
        else:
            return f"[{self.l},{self.r}]"

    def __add__(self,r : 'Node') -> 'Node':
        for n in self:
            n.depth += 1
        for n in r:
            n.depth += 1
        s = Node(l=self, r=r)
        s.reduce()
        return s

    def reduce(self):
        re = True
        while re:
            re = False
            # explode nodes with depth of 4 (cannot exceed 4 as would already be exploded)
            nodes = list(iter(self))
            for i, node in enumerate(nodes):
                if node.depth == 4:
                    # node should be the left node of the pair, so find the parent
                    parent = self.find_parent(node)
                    if i > 0:
                        # does a left number exist?
                        left = nodes[i - 1]
                        left.v += parent.l.v
                    if i < len(nodes) - 2:
                        # does a right number exist?
                        # (-2/+2 as i is the _left_ so + 1 is _right_ + 2 is the next on the right)
                        right = nodes[i + 2]
                        right.v += parent.r.v
                    parent.l = None # make parent a value node
                    parent.r = None
                    parent.v = 0
                    parent.depth = 3
                    re = True
                    break # we want to start again from the beginning
            if not re:
                # if we didn't explode, try splitting nodes over 10
                for node in self:
                    if node.v >= 10:
                        parent = self.find_parent(node)
                        pair = Node.from_list([node.v // 2, (node.v - node.v // 2)],depth=node.depth + 1)
                        if parent.l is node:
                            parent.l = pair
                        elif parent.r is node:
                            parent.r = pair
                        else:
                            assert "Node failure"
                        re = True
                        break

    def find_parent(self,child):
        if self.r is child or self.l is child:
            return self
        if self.l:
            l = self.l.find_parent(child)
            if l:
                return l
            r = self.r.find_parent(child)
            if r:
                return r
        return None


    def magnitude(self):
        if self.v is not None:
            return self.v
        else:
            return 3 * self.l.magnitude() + 2 * self.r.magnitude()

def part1(sfs):
    sum = sfs[0]
    for sf in sfs[1:]:
        sum += sf
    return sum.magnitude()

def part2(lines):
    # start from lines, as we mutate l, r when we add them
    # (this probably isn't best practise)
    sums = [Node.from_string(l) + Node.from_string(r) for l in lines for r in lines]
    magnitudes = [x.magnitude() for x in sums]
    return max(magnitudes)

def parse(lines):
    return [Node.from_string(line) for line in lines]

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
    if p1 == 4140:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_lines)
    print("Part 2")
    print("======")
    if p2 == 3993:
        print(p2)
        print(part2(lines))
    else:
        print(f"failed - {p2}")

@pytest.mark.parametrize('s',[("[1,2]")])
def test_parse(s):
    assert str(Node.from_string(s)) == s

@pytest.mark.parametrize('l,r,s',[("[1,2]","[[3,4],5]","[[1,2],[[3,4],5]]")])
def test_basic_addition(l,r,s):
    assert str(Node.from_string(l) + Node.from_string(r)) == s
@pytest.mark.parametrize('l,r,s', [("[[[[4,3],4],4],[7,[[8,4],9]]]","[1,1]","[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
                        ("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]","[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]","[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"),
                        ("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]","[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]","[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"),
                        ("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]","[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]","[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"),
                        ("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]","[7,[5,[[3,8],[1,4]]]]","[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]"),
                        ("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]","[[2,[2,2]],[8,[8,1]]]","[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]"),
                        ("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]","[2,9]","[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]"),
                        ("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]","[1,[[[9,3],9],[[9,0],[0,7]]]]","[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]"),
                        ("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]","[[[5,[7,4]],7],1]","[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]"),
                        ("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]","[[[[4,2],2],6],[8,7]]","[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")])
def test_reduced_addition(l,r,s):
    assert str(Node.from_string(l) + Node.from_string(r)) == s
@pytest.mark.parametrize('sf,m',[("[[1,2],[[3,4],5]]",143),
                                ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",1384),
                                ("[[[[1,1],[2,2]],[3,3]],[4,4]]",445),
                                ("[[[[3,0],[5,3]],[4,4]],[5,5]]",791),
                                ("[[[[5,0],[7,4]],[5,5]],[6,6]]",1137),
                                ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",3488)])
def test_magnitude(sf,m):
    assert(Node.from_string(sf).magnitude()) == m
