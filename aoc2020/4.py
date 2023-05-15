#!/usr/bin/env python3

import sys
# from collections import defaultdict, deque
import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache

def part1(documents):
    count = 0
    required = set(['byr','iyr','eyr','hgt','hcl','ecl','pid']) # don't require cid
    for doc in documents:
        keys = set(doc.keys())
        if (keys & required) == required:
            count += 1
    return count

def check_height(hgt):
    if hgt[-2:] == 'cm':
        return 150 <= int(hgt[:-2]) <= 193
    elif hgt[-2:] == 'in':
        return 59 <= int(hgt[:-2]) <= 76

re_hcl = re.compile(r'#[0-9a-f]{6}$')
re_pid = re.compile(r'[0-9]{9}$')

def check_doc(doc):
    byr = 1920 <= int(doc['byr']) <= 2002 and doc['byr'].isnumeric()
    iyr = 2010 <= int(doc['iyr']) <= 2020 and doc['iyr'].isnumeric()
    eyr = 2020 <= int(doc['eyr']) <= 2030 and doc['eyr'].isnumeric()
    hgt = check_height(doc['hgt'])
    hcl = re_hcl.match(doc['hcl'])
    ecl = doc['ecl'] in ['amb','blu','brn','gry','grn','hzl','oth']
    pid = re_pid.match(doc['pid'])
    return byr and iyr and eyr and hgt and hcl and ecl and pid

def part2(documents):
    count = 0
    required = set(['byr','iyr','eyr','hgt','hcl','ecl','pid']) # don't require cid
    for doc in documents:
        keys = set(doc.keys())
        if (keys & required) == required:
            count += 1 if check_doc(doc) else 0
    return count

def parse(data):
    raw_documents = [ [l for l in doc.split('\n')] for doc in data.split('\n\n')]
    documents = []
    for document in raw_documents:
        doc = {}
        for line in document:
            doc |= {kv.split(':')[0]:kv.split(':')[1] for kv in line.split(' ')}
        documents.append(doc)
    return documents

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
    if p1 == 2:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 2:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

def test_valid():
    data = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
    for doc in parse(data):
        assert check_doc(doc)

def test_invalid():
    data = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
    for doc in parse(data):
        assert not check_doc(doc)
