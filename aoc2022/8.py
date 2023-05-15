#!/usr/bin/env python3

import sys
overlaps = 0
with open(sys.argv[1]) as infile:
    while(team := infile.readline().rstrip()):
        elf_one, elf_two = team.split(',')
        elf_one_assignment = [int(x) for x in elf_one.split('-')]
        elf_two_assignment = [int(x) for x in elf_two.split('-')]
        overlap = ( elf_two_assignment[0] <= elf_one_assignment[0] <= elf_two_assignment[1]
                    or elf_two_assignment[0] <= elf_one_assignment[1] <= elf_two_assignment[1]
                    or elf_one_assignment[0] <= elf_two_assignment[0] <= elf_one_assignment[1]
                    or elf_one_assignment[0] <= elf_two_assignment[1] <= elf_one_assignment[1] )
        # print(f"team: {team} one: {elf_one} {elf_one_assignment} two: {elf_two} {elf_two_assignment}  overlap: {overlap}")
        if overlap:
           overlaps = overlaps + 1
print(overlaps)
