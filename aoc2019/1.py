#!/usr/bin/env python3

import sys

# from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
# from dataclasses import dataclass, field
# from functools import cache,lru_cache


def fuel(mass: int) -> int:
    """Fuel required to launch a given *module* is based on its *mass*.
    Specifically, to find the fuel required for a module,
    take its mass, divide by three, round down, and subtract 2."""
    return (mass // 3) - 2


def part1(modules: list[int]) -> int:
    """To find it, individually calculate the fuel needed
    for the mass of each module (your puzzle input),
    then add together all the fuel values."""
    return sum([fuel(module) for module in modules])


def fuel_t(mass: int) -> int:
    """Any mass that would require *negative fuel* should instead
    be treated as if it requires *zero fuel*"""
    return max(fuel(mass), 0)


def fuel_tyranny(mass: int) -> int:
    """Fuel itself requires fuel just like a module
    - take its mass, divide by three, round down, and subtract 2.
    However, that fuel *also* requires fuel, and *that* fuel requires fuel, and so on.
    """
    additional_fuel = fuel_t(mass)
    total_fuel = additional_fuel
    while additional_fuel > 0:
        additional_fuel = fuel_t(additional_fuel)
        total_fuel += additional_fuel
    return total_fuel


def part2(modules: list[int]) -> int:
    """Sum the fuel required for all the modules
    when also taking into account the mass of the added fuel"""
    return sum([fuel_tyranny(module) for module in modules])


def parse(lines: list[str]) -> list[int]:
    return [int(line) for line in lines]


if __name__ == "__main__":
    test_infile = sys.argv[0][:-3] + "-test.txt"
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split("\n")]
    test_parsed = parse(test_lines)

    infile = sys.argv[0][:-3] + "-input.txt"
    data = open(infile).read().strip()
    lines = [x for x in data.split("\n")]
    parsed = parse(lines)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 656:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 968:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")
