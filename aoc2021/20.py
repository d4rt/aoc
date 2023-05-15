#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
import numpy as np
# from dataclasses import dataclass, field
pixel_dict = {".": 0, "#":1}

def enhance(image, enhancement,ext=0,new=0):
    ext_image = np.zeros((image.shape[0] + 4, image.shape[0] + 4),dtype=int)
    ext_image.fill(ext)
    ext_image[2:2+len(image),2:2+len(image[0])] = image
    new_image = np.zeros_like(ext_image)
    new_image.fill(new)
    for i in range(1,len(image) + 3):
        for j in range(1, len(image) + 3):
            bin = np.sum([digit * 2 ** i for i, digit in enumerate(ext_image[i-1:i+2,j-1:j+2].reshape(-1)[::-1])])
            new_image[i,j] = enhancement[bin]
    return new_image

def part1(trench):
    enhancement, image = trench
    one = enhance(image,enhancement,new=enhancement[0])
    two = enhance(one,enhancement,ext=enhancement[0],new=enhancement[511*enhancement[0]])
    return np.count_nonzero(two)

def part2(trench):
    enhancement, image = trench
    new = enhancement[0]
    ext = 0
    for i in range(50):
       image = enhance(image,enhancement,new=new,ext=ext)
       new = ext
       ext = enhancement[511*new]
    return np.count_nonzero(image)

def parse(data):
    blocks = [x for x in data.split('\n\n')]
    enhancement = np.asarray([pixel_dict[p] for p in blocks[0]],dtype=int)
    image = np.asarray([[pixel_dict[p] for p in line] for line in blocks[1].split('\n')],dtype=int)
    return (enhancement,image)

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
    if p1 == 35:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 3351:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
