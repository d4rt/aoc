#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def build_dict(ingredients, allergens):
    i_sets = [{ i for i in ins } for ins in ingredients]
    a_sets = [{ a for a in als } for als in allergens]
    for als in allergens:
        for allergen in als:
            # try to build a mapping
            candidates = set()
            for ins, allers in zip(ingredients, allergens):
                if allergen in allers:
                    if candidates == set():
                        candidates = set(ins)
                    else:
                        candidates &= set(ins)
                    if candidates == set():
                        raise
                    if len(candidates) == 1:
                        d = {allergen : candidates.pop()}
                        remaining_ingredients = [[i for i in ins if i != d[allergen]] for ins in ingredients]
                        remaining_allergens = [[a for a in als if a != allergen] for als in allergens]
                        if all([als == [] for als in remaining_allergens]):
                            return d
                        else:
                            return d | build_dict(remaining_ingredients, remaining_allergens)

def part1(foods):
    ingredients, allergens = foods
    mapping = build_dict(ingredients, allergens)
    rev_mapping = {v:k for k,v in mapping.items()}
    # each allergen is found in exactly one ingredient
    # allergens are not always marked
    count = 0
    for ins in ingredients:
        for i in ins:
            if i not in rev_mapping:
                count += 1
    return count
def part2(foods):
    ingredients, allergens = foods
    mapping = build_dict(ingredients, allergens)
    rev_mapping = {v:k for k,v in mapping.items()}
    return ','.join([mapping[m] for m in sorted(mapping)])

def parse(lines):
    ingredients = []
    allergens  = []
    for line in lines:
        i,a = line.split('(')
        i = i[:-1].split(' ')
        a = a[9:-1]
        a = a.split(', ')
        ingredients.append(i)
        allergens.append(a)

    return (ingredients, allergens)

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
    if p2 == 'mxmxvkd,sqjhc,fvjkl':
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
