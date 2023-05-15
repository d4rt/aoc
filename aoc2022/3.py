#!/usr/bin/env python3

import sys

scoring = { "A X" : 4, "A Y": 8, "A Z": 3,
            "B X" : 1, "B Y": 5, "B Z": 9,
            "C X" : 7, "C Y": 2, "C Z": 6,
           }

score = 0
with open(sys.argv[1]) as infile:
    for line in infile:
        score = score + scoring[line.strip()]

print(score)
