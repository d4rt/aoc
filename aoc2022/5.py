#!/usr/bin/env python3

import sys

total_priority = 0

with open(sys.argv[1]) as infile:
    for rucksack in infile:
        l = len(rucksack)
        left = rucksack[0:l // 2]
        right = rucksack[l // 2:]
        items_left = {}
        items_right = {}
        for item in left:
            if item in items_left:
                items_left[item] += 1
            else:
                items_left[item] = 1
        for item in right:
            if item in items_right:
                items_right[item] += 1
            else:
                items_right[item] = 1
        for item in items_left:
            if item in items_right:
                duplicates = item
        priority = ord(duplicates)
        # ord('a') == 97, ord('A') == 65
        if priority >= 97:
            priority = priority - 96
        else:
            priority = priority - 38
        total_priority += priority
print(total_priority)
