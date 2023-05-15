#!/usr/bin/env python3
for digit in range(1,10):
    w = digit
    x = 1
    y = 39 + digit
    z = 39 + digit
    print(w,x,y,z)
    w = digit
    w = 0
    x = 0
    x = x % 26
    z = 0 // 1
    x += 10
    x = 1 if x == w else 0
    x = 1 if x == 0 else 0
    y = 0
    y = 25
    y = y * x
    z += y
    print(w,x,y,z)
