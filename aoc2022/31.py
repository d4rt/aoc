#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
from copy import deepcopy

# for caching distances
def memoize(f):
    memo = {}
    def helper(x,y):
        if (x,y) not in memo:
            memo[(x,y)] = f(x,y)
        return memo[(x,y)]
    return helper

# boilerplate : read file
infile = sys.argv[1] if len(sys.argv)>1 else (sys.argv[0][:-3] + '-test.txt')
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]
# parse
v_re = re.compile(r"Valve (?P<valve>..) has flow rate=(?P<rate>[0-9]+); tunnels? leads? to valves? (?P<routes>.*)")
matches = [v_re.match(line) for line in lines]
valves = [match.group('valve') for match in matches]
rates = [int(match.group('rate')) for match in matches]
valve_dict = dict(zip(valves,rates))
routes = []
for match in matches:
    rs = match.group('routes').split(', ')
    for r in rs:
        routes.append((match.group('valve'),r))

VALVE_TIME = 1
MOVE_TIME = 1
TOTAL_TIME = 30

@memoize
def distance(valve_from,valve_to):
    visited = []
    distances = {valve_from: 0}
    next_valves = deque()
    while(True):
        for route in routes:
            if route[0] == valve_from:
                if not route[1] in visited:
                    distances[route[1]] = distances[route[0]] + 1
                    if route[1] == valve_to:
                        return distances[valve_to]
                    next_valves.append(route[1])
                    visited.append(route[1])
        valve_from = next_valves.popleft()


def best_valves(location, valves_unopened, time_remaining):
    flows = {}
    for valve in valves_unopened:
        dist = distance(location,valve)
        if dist < time_remaining:
            flow = valve_total_flow(valve_dict[valve], time_remaining - dist - 1)
            if flow > 0:
                flows[valve] = flow
    s = sorted(flows.items(),key=lambda x:x[1])
    return reversed(s)


def valve_total_flow(rate, time_remaining):
    return rate * time_remaining

def max_flow(location, valves_unopened, time_remaining):
    print(f"at = {location}, valves = {valves_unopened}, time = {time_remaining}")
    total_flow = 0
    MAX_flow = 0
    MAX_flow_soln = None
    best = list(best_valves(location, valves_unopened, time_remaining))
    print(f"at = {location}, valves = {valves_unopened}, time = {time_remaining}, best = {best}")
    for b in best:
        new_time_remaining = time_remaining - distance(location,b[0]) - 1
        v_u = deepcopy(valves_unopened)
        v_u.remove(b[0])
        if v_u is not None and len(v_u) > 0 and time_remaining > 1:
            recurse = max_flow(b[0],v_u,new_time_remaining)
            print(f"at = {location} trying = {b} subflows = {recurse}")
            if recurse is not None:
                flow = b[1] + recurse[0][1]
                if flow > MAX_flow:
                    print(f"at = {location} new max flow = {flow} with valve {b} and further {recurse}")
                    MAX_flow = max(MAX_flow, flow)
                    recurse.insert(0,(b[0], MAX_flow)) # left append
                    MAX_flow_soln = recurse
            else:
                flow = b[1]
                if flow > MAX_flow:
                    print(f"at = {location} new max flow = {flow} with valve {b}")
                    MAX_flow = max(MAX_flow,flow)
                    MAX_flow_soln = [(b[0], MAX_flow)]
        else:
            flow = b[1]
            if flow > MAX_flow:
                print(f"at = {location} new max flow = {flow} with valve {b}")
                MAX_flow = max(MAX_flow,flow)
                MAX_flow_soln = [(b[0], MAX_flow)]
    return MAX_flow_soln

def part1():
    v_u = [v for v in valves if valve_dict[v] > 0] # we never need to consider valves with no flow, small optimisation
    print(f"part 1 {v_u}")
    l = 'AA'
    time_r = TOTAL_TIME
    p1 = max_flow(l, v_u, time_r)
    print(p1)
    time_r = TOTAL_TIME - 4
    l = 'AA'
    elf = max_flow(l, v_u, time_r)
    elf_valves = [x[0] for x in elf]
    v_u = [v for v in valves if valve_dict[v] > 0 and v not in elf_valves] # we never need to consider valves with no flow, small optimisation
    elephant = max_flow(l,v_u, time_r)
    print(elf)
    print(elephant)


part1()
