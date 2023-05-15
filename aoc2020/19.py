#!/usr/bin/env python3

import sys
from collections import defaultdict
# import re
# from tqdm import tqdm
# import numpy as np
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable
from functools import cache
from parsy import forward_declaration, string, seq
from itertools import count

# adapted from https://blog.bruce-hill.com/packrat-parsing-from-scratch
@dataclass
class packrat_match:
    """Class for matches from packrat parsers
       start: inclusive start point of match (i.e. text[start:end] )
       end: exclusive end point (i.e. text[start:end])"""
    text: str
    start: int
    end: int
    children: list['packrat_match']

@dataclass
class packrat_grammar:
    rules: dict
    def ref(key: str) -> Callable[[str,int],packrat_match]:
        def impl(text: str, pos: int) -> packrat_match:
            return rules[key](text, pos)
        return impl

def packrat_literal(literal: str) -> Callable[[str,int],packrat_match]:
    """Packrat match a literal string, None if no match"""
    @cache
    def impl(text: str, pos: int) -> packrat_match:
        if text.startswith(literal, pos):
            return packrat_match(text, pos, pos + len(literal))
    return impl

def packrat_sequence(patterns: list[Callable[[str,int],packrat_match]]) -> Callable[[str,int],packrat_match]:
    """Match a series of patterns, in order"""
    @cache
    def impl(text: str, pos: int) -> packrat_match:
        start = pos
        children = []
        for pattern in patterns:
            res = pattern(text, pos)
            if res is None:
                return None
            children.append(res)
            pos = res.end
        return packrat_match(text, start, pos, children)
    return impl

def packrat_or(patterns: list[Callable[str,int],packrat_match]):
    @cache
    def impl(text: str, pos: int) -> packrat_match:
        for pattern in patterns:
            res = pattern(text,pos)
            if res:
                return res
    return impl

RULES = {}
def build_custom_parser(rules):
    for rule in rules:
        RULES[rule] = parser_rule(rules[rule])

def const_parser(char):
    def impl(s: str,p: int):
        if p >= len(s):
            return (False, p)
        if s[p] == char:
            #print(f"{p} const {char} match")
            return (True, p + 1)
        else:
            #print(f"{p} const {char} fail")
            return (False, p)
    return impl

def sequence_rule(sequence):
    rules = sequence.split(' ')
    def impl(s: str,p: int):
        c = p
        for rule in rules:
            #print(f"{c} sequence {rule}")
            m, c = RULES[rule](s,c)
            if not m:
                #print(f"{c} sequence {rule} failed back to {p}")
                return (False, p)
        if not m:
            #print(f"{c} sequence {rule} failed back to {p}")
            return (False, p)
        #print(f"{c} sequence match")
        return (m, c)
    return impl

def alternating_rule(sequence):
    left, right = sequence.split(' | ')
    left = left.split(' ')
    right = right.split(' ')
    def impl(s: str, p: int, right: bool = True):
        c = p
        for rule in left:
            #print(f"{c} left {rule}")
            m, c, _ = RULES[rule](s,c)
            if not m:
                break
        if m:
            return (m, c, True)
        c = p
        for rule in right:
            #print(f"{c} right {rule}")
            m, c, _ = RULES[rule](s,c)
            if not m:
                return (False, p, False)
        return (m, c, False)
    return impl

def parser_rule(rule):
    rule = rule.strip()
    q = rule.find('"')
    if q != -1:
        return const_parser(rule[q + 1])
    q = rule.find('|')
    if q != -1:
        return alternating_rule(rule)
    else:
        return sequence_rule(rule)


def build_parser(rules,default_rule = '0'):
    parsers = {k: forward_declaration() for k in rules}
    for rule in rules:
        parsing_string = rules[rule].strip()
        q = parsing_string.find('"')
        if q != -1:
            c = parsing_string[q + 1]
            parsers[rule].become(string(c))
            continue
        q = parsing_string.find('|')
        if q != -1:
            # alternation rule
            left, right = parsing_string.split(' | ')
            lefts = left.split(' ')
            rights = right.split(' ')
            common = []
            nl = []
            nr = []
            diff = True
            for l,r in zip(lefts,rights):
                if l == r and diff:
                    common.append(l)
                else:
                    break
            common_length = len(common)
            nl = lefts[common_length:]
            nr = rights[common_length:]
            if common == []:
                parsers[rule].become(seq(*[parsers[r] for r in left.split(" ")]) | seq(*[parsers[r] for r in right.split(" ")]))
            else:
                #print(f"{rule} : {left} | {right} ")
                #print(f"{rule} : {common} + {nl} | +{nr} ")
                common_parser = seq(*[parsers[x] for x in common])
                left_parser = seq(*[parsers[x] for x in nl])
                right_parser = seq(*[parsers[x] for x in nr])
                parsers[rule].become(seq(common_parser, left_parser | right_parser))
        else:
            parsers[rule].become(seq(*[parsers[r] for r in parsing_string.split(" ")]))
    return parsers[default_rule]
def cnf(rules: dict[str,str]) -> dict[str,str]:
    new_rules = {}

    terminals = {k: v[1] for k,v in rules.items() if v[0] == '"'}

    # BIN
    new_rules = deepcopy(rules)
    for rule in new_rules:
        if rule in terminals:
            # print(f"dbg BIN: skip terminal {rule} {rules[rule]}")
            continue
        parts = rules[rule].split(' | ')
        new_parts = []
        it = count(start = 1)
        for part in parts:
            atoms = part.split(' ')
            if len(atoms) > 2:
                i = next(it)
                new_part = atoms[0] + ' ' + rule + chr(i + 64)
                for atom in atoms[1:-2]:
                    p = i
                    i = next(it)
                    rules[rule + chr(p + 64)] = atom + ' ' + rule + chr(i + 64)
                rules[rule + chr(i + 64)] = atoms[-2] + ' '  + atoms[-1]
                new_parts.append(new_part)
            else:
                new_parts.append(part)
        new_rule = ' | '.join(new_parts)
        if new_rule != rules[rule]:
            #print(f'BIN: {rule} -> {rules[rule]} -> {new_rule}')
            rules[rule] = new_rule


    # DEL
    # rules already have no nullables?
    #

    # UNIT
    # eliminate unit rules
    changed = True
    while changed:
        changed = False
        for rule in rules:
            if rule in terminals:
                #print(f"dbg UNIT: skip terminal {rule} {rules[rule]}")
                continue
            parts = rules[rule].split(' | ')
            new_parts = []
            for part in parts:
                #print(f"dbg UNIT: {rule} -> {rules[rule]} part {part}")
                atoms = part.split(' ')
                if len(atoms) == 1:
                    if atoms[0][0] != '"':
                        new_part = rules[atoms[0]]
                        #print(f"dbg UNIT: {rule} -> {rules[rule]} part {part} -> {new_part}")
                    else:
                        new_part = part
                else:
                    new_part = part
                new_parts.append(new_part)
            new_rule = ' | '.join(new_parts)
            if rules[rule] != new_rule:
                #print(f"UNIT: rule {rule} -> {rules[rule]} -> {new_rule}")
                rules[rule] = new_rule
                changed = True
    return rules
def cyk(rules: dict[str,str],s:str) -> bool:
    """Use Cocke-Younger-Kasami to parse, considering each substring
       Grammar must be CNF (i.e. only 2 subrules per rule)"""
    # https://en.wikipedia.org/wiki/CYK_algorithm
    #
    partials = [[[] for c in s ] for x in s]  # back on wp
    terminals_r = defaultdict(list)
    for rule in rules:
        parts = rules[rule].split(' | ')
        for part in parts:
            atoms = part.split(' ')
            if len(atoms) == 1:
                if atoms[0][0] == '"':
                    terminals_r[atoms[0][1]].append(rule)
    #print(terminals_r)
    rev_rules = defaultdict(list)
    for rule in rules:
        parts = rules[rule].split(' | ')
        for part in parts:
            rev_rules[part].append(rule)
    #print(rev_rules)
    # bottom row
    for i, c in enumerate(s):
        partials[0][i] = terminals_r[c]
    #print(f"terminals {partials[0]}")
    # subsequent rows
    for j in range(1,len(s)):
        #print(f"row(j) {j}")
        for i in range(len(s) - j):
            #print(f"pos(i) {i}")
            # consider each pairing and if it works
            # so for the 2nd row, it's just both items on the bottom row
            # for others we walk up and down the stacks
            for k in range(j):
                lj = k
                li = i
                rj = j - k - 1
                ri = i + k + 1
                #print(f"stacks(k) {k} ({lj},{li}) + ({rj},{ri})")
                for l in partials[lj][li]:
                    for r in partials[rj][ri]:
                        key = l + ' ' + r
                        #print(f"stacks ({lj},{li}) + ({rj},{ri}) key {key}")
                        if key in rev_rules:
                            #print(f"stacks ({lj},{li}) + ({rj},{ri}) key {key} matches {rev_rules[key]}")
                            partials[j][i].extend(rev_rules[key])
        #print(partials[j])
    return '0' in partials[len(s) - 1][0]
def part1(data):
    rules, messages = data
    matcher = build_parser(rules)
    count = 0
    for message in messages:
        try:
            parsed = matcher.parse(message)
            count += 1
            #print(f"{message}")
        except Exception as e:
            pass
    return count

def part2(data):
    rules, messages = data
    rules['8'] = '42 8 | 42'
    # decompose 11 into CNF
    rules['11'] = '42 31 | 42 11 31'
    rules = {k:v.strip() for k,v in rules.items()}
    rules = cnf(rules)
    count = 0
    for message in messages:
        res = cyk(rules, message)
        if res:
            count += 1
    return count
def parse(data):
    rules, messages = data.split('\n\n')
    rules = rules.split('\n')
    rules = [r.strip() for r in rules]
    rules = dict([x.split(':') for x in rules])
    messages = messages.split('\n')
    return (rules,messages)

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
    if p1 == 3:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    print(p2)
    print(part2(parsed))

def test_cyk():
    rules = {}
    rules['0'] = '1 2'
    rules['1'] = '"a"'
    rules['2'] = '"b"'
    s = "ab"
    assert cyk(rules,s)
    rules['3'] = '1 2'
    rules['4'] = '3 1'
    rules['5'] = '2 1'
    rules['0'] = '3 | 4'
    s = "aba"
    assert cyk(rules,s)
    s = "abba"
    assert not cyk(rules,s)

def test_cyk_block():
    rules = {
        '0': '4 6',
        '6': '1 5',
        '1': '2 3 | 3 2',
        '2': '4 4 | 5 5',
        '3': '4 5 | 5 4',
        '4': '"a"',
        '5': '"b"'
    }
    test_success = ['ababbb','abbbab']
    test_fail = ['bababa','aaabbb','aaaabbb']
    for test in test_success:
        print(test)
        assert cyk(rules,test)
    for test in test_fail:
        assert not cyk(rules,test)
