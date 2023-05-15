#!/usr/bin/env python3

import sys

def get_rucksack_items(rucksack):
    rucksack_items = {}
    for item in rucksack:
        if item in rucksack_items:
            rucksack_items[item] += 1
        else:
            rucksack_items[item] = 1
    return rucksack_items

total_priority = 0

with open(sys.argv[1]) as infile:
    while(rucksack_one := infile.readline().rstrip()):
        rucksack_two = infile.readline().rstrip()
        rucksack_three = infile.readline().rstrip()
        items_one = get_rucksack_items(rucksack_one)
        items_two = get_rucksack_items(rucksack_two)
        items_three = get_rucksack_items(rucksack_three)

        for item in items_one:
                if item in items_two:
                    if item in items_three:
                        badge = item
        priority = ord(badge)
            # ord('a') == 97, ord('A') == 65
        if priority >= 97:
            priority = priority - 96
        else:
            priority = priority - 38
        total_priority += priority
print(total_priority)
