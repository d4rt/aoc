#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm

def eval_monkey(monkey, monkeys):
    if 'val' in monkey:
        return monkey['val']
    else:
        rhs = eval_monkey(monkeys[monkey['rhs']],monkeys)
        lhs = eval_monkey(monkeys[monkey['lhs']],monkeys)
        return monkey['op'](rhs,lhs)

def op_add(r,l):
    return r + l

def op_minus(r,l):
    return r - l

def op_mult(r,l):
    return r * l

def op_div(r,l):
    return r / l
ops = {'+' : op_add, '-': op_minus, '/': op_div, '*': op_mult}
def part1(lines):
    monkeys = {}
    for monkey in lines:
        name, fun = monkey.split(':')
        fun = fun.strip()
        if fun.isnumeric():
            monkeys[name] = {'val': int(fun)}
        else:
            rhs, op, lhs = fun.split(' ')
            monkeys[name] = {'rhs' : rhs, 'op' : ops[op], 'lhs' : lhs}
    return eval_monkey(monkeys['root'],monkeys)

def part2(lines):
    monkeys = {}
    for monkey in lines:
        name, fun = monkey.split(':')
        fun = fun.strip()
        if fun.isnumeric():
            monkeys[name] = {'val': int(fun)}
        else:
            rhs, op, lhs = fun.split(' ')
            monkeys[name] = {'rhs' : rhs, 'op' : ops[op], 'lhs' : lhs}
    goals = [monkeys['root']['lhs'], monkeys['root']['rhs']]
    m = 'humn'
    others = list(monkeys.keys())
    others.remove(m)
    while(m not in goals):
        for name, monkey in monkeys.items():
            if 'rhs' in monkey:
                if monkey['rhs'] == m or monkey['lhs'] == m:
                    m = name
                    others.remove(m)
    if m == goals[0]:
        goal = eval_monkey(monkeys[goals[1]], monkeys)
    else:
        goal = eval_monkey(monkeys[goals[0]], monkeys)
    other_monkeys = dict([(m,eval_monkey(monkeys[m],monkeys)) for m in others])
    while(m != 'humn'):
        monkey = monkeys[m]
        lhs = monkey['lhs']
        rhs = monkey['rhs']
        if lhs in other_monkeys:
            if monkey['op'] == op_add:
                goal = goal - other_monkeys[lhs]
            if monkey['op'] == op_mult:
                goal = goal / other_monkeys[lhs]
            if monkey['op'] == op_div:
                goal = goal * other_monkeys[lhs]
            if monkey['op'] == op_minus:
                goal = goal + other_monkeys[lhs]
            m = monkey['rhs']
            continue

        if rhs in other_monkeys:
            if monkey['op'] == op_add:
                goal = goal - other_monkeys[rhs]
            if monkey['op'] == op_mult:
                goal = goal / other_monkeys[rhs]
            if monkey['op'] == op_div:
                goal = goal * other_monkeys[rhs]
            if monkey['op'] == op_minus:
                goal = -(goal - other_monkeys[rhs])
            m = monkey['lhs']
            continue
        print(f"stuck at ${m}")
    return goal


test_infile = sys.argv[0][:-3] + '-test.txt'
test_data = open(test_infile).read().strip()
test_lines = [x for x in test_data.split('\n')]

infile = sys.argv[0][:-3] + '-input.txt'
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]

p1 = part1(test_lines)
if p1 == 152:
    print("Part 1")
    print("======")
    print(p1)
    print(part1(lines))
    print()
else:
    print(f"failed - {p1}")
p2 = part2(test_lines)
if p2 == 301:
    print("Part 2")
    print("======")
    print(p2)
    print(part2(lines))
else:
    print(f"failed - {p2}")
