#!/usr/bin/env python3

import sys
overlaps = 0
with open(sys.argv[1]) as infile:
    while(team := infile.readline().rstrip()):
        elf_one, elf_two = team.split(',')
        elf_one_assignment = [int(x) for x in elf_one.split('-')]
        elf_two_assignment = [int(x) for x in elf_two.split('-')]
        elf_one_width = elf_one_assignment[1] - elf_one_assignment[0] + 1
        elf_two_width = elf_two_assignment[1] - elf_two_assignment[0] + 1
        if elf_one_width > elf_two_width:
            overlap = (elf_two_assignment[0] >= elf_one_assignment[0]
                      and elf_two_assignment[1] <= elf_one_assignment[1] )
        else:
            overlap = (elf_one_assignment[0] >= elf_two_assignment[0]
                      and elf_one_assignment[1] <= elf_two_assignment[1] )
        # print(f"team: {team} one: {elf_one} {elf_one_assignment} {elf_one_width} two: {elf_two} {elf_two_assignment} {elf_two_width} overlap: {overlap}")
        if overlap:
           overlaps = overlaps + 1
print(overlaps)
