#!/usr/bin/env python3

import sys
LEN = 14
LEN_MINUS_1 = LEN - 1
signal = open(sys.argv[1]).readline()
markers = []
for i in range(LEN_MINUS_1, len(signal)-LEN_MINUS_1):
    if len(set(signal[i:i+LEN])) == LEN:
        markers.append(i+LEN)

print(markers[0])
