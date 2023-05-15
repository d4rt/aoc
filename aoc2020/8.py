#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def exec_op(ip,acc,ops):
    ins = ops[ip]
    if ins[0] == 'nop':
        return (ip + 1, acc)
    if ins[0] == 'acc':
        return (ip + 1, acc + ins[1])
    if ins[0] == 'jmp':
        return (ip + ins[1], acc)

def part1(ops):
    ip = 0
    acc = 0
    run = set()
    while True:
        if ip in run:
            return acc
        run.add(ip)
        (ip,acc) = exec_op(ip,acc,ops)
def terminates(ops):
    ip = 0
    acc = 0
    run = set()
    while True:
        if ip == len(ops): # reached the instruction just outside the 'infinite loop'
            return acc
        if ip in run or ip > len(ops): # loop or jump far outside the 'infinite loop'
            return None
        run.add(ip)
        (ip,acc) = exec_op(ip,acc,ops)

def part2(ops):
    """Try changing each op and see if the program terminates normally"""
    for i, op in enumerate(ops):
        if op[0] == 'acc':
            continue
        else:
            op = ('jmp',op[1]) if op[0] == 'nop' else ('nop',op[1])
        new_ops = ops.copy()
        new_ops[i] = op
        t = terminates(new_ops)
        if t:
            return t

    

def parse_op(l):
    op, arg = l.split(" ")
    arg = int(arg)
    return (op,arg)
def parse(lines):
    return [parse_op(l) for l in lines]

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
    if p1 == 5:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 8:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
