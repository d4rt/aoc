#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def can_contain(container,containers,item):
    for subcontainer in containers[container]:
        if item in subcontainer:
            return True
    else:
        for subcontainer in containers[container]:
            if can_contain(list(subcontainer.keys())[0],containers,item):
                return True
def part1(containers):
    return sum([1 if can_contain(container,containers,'shiny gold') else 0 for container in containers])

def sum_containers(container,containers):
    sum = 0
    for subcontainer in containers[container]:
        for c, count in subcontainer.items():
           sum += count + count * sum_containers(c,containers)
    return sum

def part2(containers):
    return sum_containers('shiny gold', containers)

def parse(lines):
    container_dict = {}
    for line in lines:
        container, contains = line.split(' contain ')
        container = ' '.join(container.split(' ')[:-1])
        contains_list = []
        for items in contains.split(', '):
            if items == 'no other bags.':
                continue
            else:
                i = items.split(" ")
                contains_list.append({" ".join(i[1:-1]): int(i[0])})
        container_dict[container] = contains_list
    return container_dict


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
    if p1 == 4:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 32:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
