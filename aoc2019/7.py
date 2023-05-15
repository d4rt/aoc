#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from intcode import parse, run, Intcode
from itertools import permutations

def part2(code):
    m = 0

    for pa, pb, pc, pd, pe in permutations(range(5, 10), 5):
        a = Intcode.new(code)
        b = Intcode.new(code)
        c = Intcode.new(code)
        d = Intcode.new(code)
        e = Intcode.new(code)
        i = 0
        oa = a.step([pa, i])
        ob = b.step([pb, oa])
        oc = c.step([pc, ob])
        od = d.step([pd, oc])
        i = e.step([pe, od])
        while not a.stopped:
            oa = a.step([i])
            ob = b.step([oa])
            oc = c.step([ob])
            od = d.step([oc])
            pi = i
            i = e.step([od])
        m = max(m, pi)
    return m


def part1(code):
    m = 0

    for pa, pb, pc, pd, pe in permutations(range(5), 5):
        a = run(code, intcode_input=[pa, 0])
        b = run(code, intcode_input=[pb, a[0]])
        c = run(code, intcode_input=[pc, b[0]])
        d = run(code, intcode_input=[pd, c[0]])
        e = run(code, intcode_input=[pe, d[0]])
        m = max(m, e[0])
    return m


if __name__ == "__main__":
    infile = sys.argv[0][:-3] + "-input.txt"
    data = open(infile).read().strip()
    lines = [x for x in data.split("\n")]
    parsed = parse(lines)
    print("Part 1")
    print("======")
    print(part1(parsed))
    print("Part 2")
    print("======")
    print(part2(parsed))


def test_thruster_1():
    code1 = parse(["3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"])
    assert 43210 == part1(code1)


# def test_thruster_debug_1():
#     code1 = parse(["3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"])
#     pa = 4
#     pb = 3
#     pc = 2
#     pd = 1
#     pe = 0

#     no_copy = code1.copy()
#     assert code1 == no_copy
#     a = run(code1, intcode_input=[pa, 0], debug=True)
#     assert code1 == no_copy
#     b = run(code1, intcode_input=[pb, a[0]], debug=True)
#     assert code1 == no_copy
#     c = run(code1, intcode_input=[pc, b[0]], debug=True)
#     assert code1 == no_copy
#     d = run(code1, intcode_input=[pd, c[0]], debug=True)
#     assert code1 == no_copy
#     e = run(code1, intcode_input=[pe, d[0]], debug=True)
#     assert code1 == no_copy


#     assert e[0] == 43210
def test_thruster_2():
    code2 = parse(
        ["3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"]
    )
    assert 54321 == part1(code2)


def test_thruster_3():
    code3 = parse(
        [
            "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
        ]
    )
    assert 65210 == part1(code3)


def test_thruster_part2_1():
    code = parse(
        [
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
        ]
    )
    assert 139629729 == part2(code)


def test_thruster_part2_2():
    code = parse(
        [
            "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
        ]
    )
    assert 18216 == part2(code)
