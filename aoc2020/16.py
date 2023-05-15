#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
import re
# from tqdm import tqdm
# import numpy as np
from dataclasses import dataclass, field
# from functools import cache,lru_cache

def column_mapping(rules,tickets):
    pass

def check_valid(rule, value):
   return rule['min1'] <= value <= rule['max1'] or rule['min2'] <= value <= rule['max2']

def trivially_invalid_tickets(rules,tickets):
    invalid = 0
    for ticket in tickets:
        valid = True
        for value in ticket:
            valid_value = False
            for rule in rules:
                if check_valid(rule,value):
                    valid_value = True
            if not valid_value:
                invalid += value
    return invalid

def filter_valid_tickets(rules,tickets):
    valid = []
    for ticket in tickets:
        for value in ticket:
            valid_value = False
            for rule in rules:
                if check_valid(rule,value):
                    valid_value = True
            if not valid_value:
                break
        if valid_value:
            valid.append(ticket)
    return valid

def set_map(possibles: dict):
    ranking = {x:len(possibles[x]) for x in possibles}
    s = sorted(ranking, key=ranking.get)
    rule = s[0]
    for possibility in possibles[rule]:
        if len(possibles) == 1:
            return {rule: possibility}
        new_possibles = possibles.copy()
        new_possibles.pop(rule)
        for k in new_possibles:
            new_possibles[k] -= set([possibility])
        rec = set_map(new_possibles)
        if rec:
            return rec | {rule: possibility}
    return None


def build_rule_mapping(rules,valid_tickets):
    mapping = {}
    possibles = {}
    for rule in rules:
        possible = set(range(len(valid_tickets[0])))
        for ticket in valid_tickets:
            for field in possible.copy():
                if not check_valid(rule, ticket[field]):
                    possible.remove(field)
        possibles[rule['rule_name']] = possible
    return set_map(possibles)



def part1(data):
    rules, ticket, nearby = data
    return trivially_invalid_tickets(rules, nearby)

def part2(data):
    rules, ticket, nearby = data
    valid_tickets = filter_valid_tickets(rules,nearby)
    mapping = build_rule_mapping(rules,valid_tickets)
    departure = 1
    for m in mapping:
        if m[:9] == 'departure':
            departure *= ticket[mapping[m]]
    return departure

re_rule = re.compile(r"(?P<rule_name>.*): (?P<min1>\d+)-(?P<max1>\d+) or (?P<min2>\d+)-(?P<max2>\d+)")
def parse(data):
    raw_rules, ticket, nearby = data.split('\n\n')[:3]
    rules = []
    for rule in raw_rules.split('\n'):
        match = re_rule.match(rule)
        if match:
            rule_dict = match.groupdict()
            for k in rule_dict:
                if rule_dict[k].isnumeric():
                    rule_dict[k] = int(rule_dict[k])
            rules.append(rule_dict)
    ticket = [int(x) for x in ticket.split('\n')[1].split(',')]
    nearby = [[int(x) for x in t.split(',')] for t in nearby.split('\n')[1:]]
    return (rules,ticket,nearby)

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
    if p1 == 71:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 1:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
