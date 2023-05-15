#!/usr/bin/env python3

import sys

scoring = { "A X" : 0+3, "A Y": 3+1, "A Z": 6+2,
            "B X" : 0+1, "B Y": 3+2, "B Z": 6+3,
            "C X" : 0+2, "C Y": 3+3, "C Z": 6+1,
           }

score = 0
with open(sys.argv[1]) as infile:
    for line in infile:
        score = score + scoring[line.strip()]

print(score)
