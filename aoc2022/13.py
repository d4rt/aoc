#!/usr/bin/env python3

import sys
import re

re_cd_abs = re.compile(r"\$ cd /")
re_cd_up = re.compile(r"\$ cd \.\.")
re_cd_dir = re.compile(r"\$ cd (?P<dir>.*)")
re_file = re.compile(r"(?P<size>[0-9]+) (?P<file>.*)")
re_dir = re.compile(r"dir (?P<dir>.*)")
re_ls= re.compile(r"\$ ls")

cd = "/"
files = {}
directories = {'/' : {'files': 0, 'subdir': [], 'sd_size': 0, 'total': 0 }}

with open(sys.argv[1]) as infile:
    while(line := infile.readline().rstrip()):
        match = re_cd_abs.match(line)
        if match:
            cd = "/"
            continue
        match = re_cd_up.match(line)
        if match:
            cd = '/'.join(cd.split('/')[:-2]) + '/'
            continue
        match = re_cd_dir.match(line)
        if match:
            cd = cd + match.group('dir') + '/'
            if not cd in directories:
                directories[cd] = {'files': 0, 'subdir': [], 'sd_size': 0, 'total': 0 }
            continue
        match = re_file.match(line)
        if match:
            file = cd + match.group('file')
            files[file] = int(match.group('size'))
            continue
        match = re_dir.match(line)
        if match:
            dir = cd + match.group('dir') + '/'
            directories[cd]['subdir'].append(dir)
            if dir not in directories:
                directories[dir] = {'files': 0, 'subdir': [], 'sd_size': 0, 'total': 0 }
            continue
        match = re_ls.match(line)
        if match:
            # I don't think we need do anything here
            continue

for f in files.keys():
    dir = '/'.join(f.split('/')[:-1]) + '/'
    directories[dir]['files'] = directories[dir]['files'] + files[f]


for d in sorted(directories.keys())[::-1]:
    for s in directories[d]['subdir']:
        directories[d]['sd_size'] = directories[d]['sd_size'] + directories[s]['total']
    directories[d]['total'] = directories[d]['files'] + directories[d]['sd_size']

used = 0
for d, dir in directories.items():
    if dir['total'] <= 100000:
        used = used + dir['total']

print(used)
