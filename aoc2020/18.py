#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from operator import add, mul
import pytest
from parsy import regex, string, seq, generate, success

def expr_eval(expr: str) -> int:
    expr = expr.replace('('," ( ").replace(")"," ) ")
    l = expr.split(' ')
    return list_eval([x for x in l if x != ''])[0]

def adv_expr_eval(s: str) -> int:
    number = regex(r"[0-9]+").map(int)
    lb = string("(")
    rb = string(")")
    @generate
    def adds():
        res = yield simple # number or bracketed expression
        op = string(' + ')
        while True:
            operation = yield op | success("") #still not 100% clear what success does here?
            if not operation:
                break
            oper = yield simple # number or bracketed expression
            res += oper
        return res
    @generate
    def muls():
        res = yield adds
        op = string(' * ')
        while True:
            operation = yield op | success("")
            if not operation:
                break
            oper = yield adds # higher precedence
            res *= oper
        return res
    expr = muls # lower precedence
    simple = (lb >> expr << rb) | number
    return expr.parse(s)



def list_eval(l: list[str], offset = 0) -> int:
    i = offset
    val = None
    while i < len(l):
        if l[i] == '(':
            if val is None:
                val, offset = list_eval(l,i + 1)
            else:
                ret, offset = list_eval(l, i + 1)
                val = op(val,ret)
            i = offset + 1
            continue
        if l[i] == ')':
            return val, i
        if l[i].isnumeric():
            if val is None:
                val = int(l[i])
            else:
                ret = int(l[i])
                val = op(val,ret)
        if l[i] == '+':
            op = add
        if l[i] == '*':
            op = mul
        i += 1
    return val, i



def part1(lines):
    return sum([expr_eval(e) for e in lines])
def part2(lines):
    return sum([adv_expr_eval(e) for e in lines])

def parse(lines):
    return lines

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
    if p1 == 26335:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 693891:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

@pytest.mark.parametrize("input,expected", [("1 + 2 * 3 + 4 * 5 + 6",71),("2 * 3 + (4 * 5)",26),("5 + (8 * 3 + 9 + 3 * 4 * 3)",437),("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",12240),("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",13632)])
def test_eval(input,expected):
    assert expr_eval(input) == expected

@pytest.mark.parametrize("input,expected", [("1 + 2", 3),("2 * 3", 6),("1 + 2 * 3 + 4 * 5 + 6",231),("2 * 3 + (4 * 5)",46),("5 + (8 * 3 + 9 + 3 * 4 * 3)",1445),("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",669060),("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",23340)])
def test_adv_eval(input,expected):
    assert adv_expr_eval(input) == expected
