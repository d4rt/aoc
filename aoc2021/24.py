#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache
from tr import python_block
def try_number(n,instructions,zero_x_y=False):
    register = {'w': 0, 'x': 0,'y': 0,'z': 0}
    s = str(n)
    nd = 0
    for i in instructions:
        if i[0] == 'inp':
            register[i[1]] = int(s[nd])
            nd +=1
            register['x'] = 0
            register['y'] = 0
            continue
        if i[0] == 'add':
            if i[2] not in register:
                register[i[1]] += int(i[2])
            else:
                register[i[1]] += register[i[2]]
            continue
        if i[0] == 'mul':
            if i[2] not in register:
                register[i[1]] *= int(i[2])
            else:
                register[i[1]] *= register[i[2]]
            continue
        if i[0] == 'div':
            if i[2] not in register:
                register[i[1]] //= int(i[2])
            else:
                register[i[1]] //= register[i[2]]
            continue
        if i[0] == 'mod':
            if i[2] not in register:
                register[i[1]] %= int(i[2])
            else:
                register[i[1]] %= register[i[2]]
            continue
        if i[0] == 'eql':
            if i[2] not in register:
                register[i[1]] = 1 if register[i[1]] == int(i[2]) else 0
            else:
                register[i[1]] = 1 if register[i[1]] == register[i[2]] else 0
            continue
    return register['z']

def eval_block(instructions,w=0,z=0):
    register = {'w': w, 'x': None,'y': None,'z': z}
    for i in instructions:
        if len(i) != 3:
            continue
        ins = i[0]
        dst = i[1]
        srct = i[2]
        src = register[srct] if srct in register else int(srct)
        if ins == 'add':
            register[dst] += src
        if ins == 'mul':
            if src == 0:
                register[dst] = 0
            else:
                register[dst] *= src
        if ins == 'div':
            register[dst] //= src
        if ins == 'mod':
            register[dst] %= src
        if ins == 'eql':
            register[dst] = 1 if register[dst] == src else 0
    return register['z']

def z_target(block,z,max_z):
    states = {}
    for zin in tqdm(range(max_z)):
       for digit in range(1,10):
           zout = eval_block(block,z=zin,w=digit)
           if zout == z:
               if digit in states:
                   states[digit].append(zin)
               else:
                   states[digit] = [zin]
    return states
dfs_ztarget_cache = {}
def dfs_ztarget(instructions, z_targets, digit, history = []):
    if (digit,z_targets) in dfs_ztarget_cache:
        return dfs_ztarget_cache[(digit,z_targets)]
    block = instructions[digit]
    print(f"{' ' * (14 - digit)} dfs_ztarget {z_targets} {digit} {history}")
    if digit == 0:
        z_max = 0
    else:
        z_max = min(26 ** (7-abs(7-digit)),10000)
    for w in range(9,0,-1):
        for zin in range(0,z_max):
            zout = eval_block(block,w=w,z=zin)
            if zout == z_targets:
                if digit > 0:
                    my_history = history.copy()
                    my_history.insert(0,w)
                    dfs = dfs_ztarget(instructions,zin,digit - 1,my_history)
                    if dfs is not None:
                        dfs_ztarget_cache[(digit,z_targets)] = dfs
                        return dfs
                else:
                    my_history = history.copy()
                    my_history.insert(0,w)
                    return my_history
    dfs_ztarget_cache[(digit,z_targets)] = None
    return None

def unwind_stack(s):
    l = []
    while s > 0:
        l.append(s % 26)
        s = (s - (s % 26)) // 26
    return l


def part1(instructions):
    # try 14 digit numbers starting at 9..9
    # evaluate all states for the first digit
    # return(dfs_ztarget(instructions,0,13))
    # states = {}
    # for i in range(14):
    #    for z in range(26):
    #        # try all states of z - determine if we add to stack or if we pop off
    #        # is it consistent for every digit / value of z?
    #        for digit in range(9,0,-1):
    #            res = eval_block(instructions[i],w=digit,z=z)
    #            res2 = eval_block(instructions[i],w=digit,z=z*26 + z)
    #            s = unwind_stack(res)
    #        if i == 0 and z > 0:
    #            break
    # must pop - 3, 5, 9, 10, 11, 12, 13
    # pushes   - 2, 4, 8,  7,  6,  1,  0
    digits = [None] * 14
    zs = [None] * 15
    zs[0] = 0
    ij = [(0,13),(1,12),(2,3),(4,5),(6,11),(7,10),(8,9)]
    digits = recurse_stack_solve(instructions,ij,zs,digits)
    digits_s = [str(i) for i in digits]
    print(''.join(digits_s))
    z = 0
    for i in range(14):
        z = python_block(i,w=digits[i],z=z)
        print(f"{i}: {digits[i]} {z} {unwind_stack(z)}")

def recurse_stack_solve(instructions,ij,zs,digits):
    i,j = ij[0]
    print(f"recurse stack solve ij {i} {j} {zs[i]}")
    for di in range(9,0,-1):
        for dj in range(9,0,-1):
            push = python_block(i,w=di,z=zs[i])
            pop = python_block(j,w=dj,z=push)
            if pop == zs[i]:
                print(f"rss found soln {di}, {dj}, checking rest")
                digits[i] = di
                zs[i+1] = push
                digits[j] = dj
                zs[j+1] = pop
                if len(ij) == 1:
                    return digits
                else:
                    solve = recurse_stack_solve(instructions,ij[1:],zs,digits)
                if solve:
                    return digits
    return None
def min_stack_solve(ij,zs,digits):
    i,j = ij[0]
    print(f"recurse stack solve ij {i} {j} {zs[i]}")
    for di in range(1,10):
        for dj in range(1,10):
            push = python_block(i,w=di,z=zs[i])
            pop = python_block(j,w=dj,z=push)
            if pop == zs[i]:
                print(f"rss found soln {di}, {dj}, checking rest")
                digits[i] = di
                zs[i+1] = push
                digits[j] = dj
                zs[j+1] = pop
                if len(ij) == 1:
                    return digits
                else:
                    solve = min_stack_solve(ij[1:],zs,digits)
                if solve:
                    return digits
    return None

def part2(lines):
    digits = [None] * 14
    zs = [None] * 15
    zs[0] = 0
    ij = [(0,13),(1,12),(2,3),(4,5),(6,11),(7,10),(8,9)]
    digits = min_stack_solve(ij,zs,digits)
    digits_s = [str(i) for i in digits]
    print(''.join(digits_s))
    z = 0
    for i in range(14):
        z = python_block(i,w=digits[i],z=z)
        print(f"{i}: {digits[i]} {z} {unwind_stack(z)}")

def parse(data):
    blocks = data.split('inp w\n')
    instruction_blocks = [ [i.split(' ')  for i in block.split('\n')] for block in blocks[1:] ]
    print(instruction_blocks)
    return instruction_blocks

if __name__ == '__main__':
    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    lines = [x for x in data.split('\n')]
    parsed  = parse(data)
    print("Part 1")
    print("======")
    if True:
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    print("Part 2")
    print("======")
    if True:
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
