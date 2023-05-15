#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
# import re
# from tqdm import tqdm
# import numpy as np
from dataclasses import dataclass, field
from queue import PriorityQueue
from frozendict import frozendict
from functools import cache,lru_cache
dbg = lambda x: None
costs = {'A': 1, 'B':10, 'C':100, 'D':1000}
distances = {'a0': {'h0':  4, 'h1': 3, 'h2': 3, 'h3': 5, 'h4': 7, 'h5': 9, 'h6': 10},
             'a1': {'h0':  3, 'h1': 2, 'h2': 2, 'h3': 4, 'h4': 6, 'h5': 8, 'h6': 9},
             'b0': {'h0':  6, 'h1': 5, 'h2': 3, 'h3': 3, 'h4': 5, 'h5': 7, 'h6': 8},
             'b1': {'h0':  5, 'h1': 4, 'h2': 2, 'h3': 2, 'h4': 4, 'h5': 6, 'h6': 7},
             'c0': {'h0':  8, 'h1': 7, 'h2': 5, 'h3': 3, 'h4': 3, 'h5': 5, 'h6': 6},
             'c1': {'h0':  7, 'h1': 6, 'h2': 4, 'h3': 2, 'h4': 2, 'h5': 4, 'h6': 5},
             'd0': {'h0': 10, 'h1': 9, 'h2': 7, 'h3': 5, 'h4': 3, 'h5': 3, 'h6': 4},
             'd1': {'h0':  9, 'h1': 8, 'h2': 6, 'h3': 4, 'h4': 2, 'h5': 2, 'h6': 3}}
direct_paths = {'h0': ['h1'],
                'h1': ['h0','h2','a1'],
                'h2': ['h1','h3','a1','b1'],
                'h3': ['h2','h4','b1','c1'],
                'h4': ['h3','h5','c1','d1'],
                'h5': ['h4','h6','d1'],
                'h6': ['h5']}
direct_paths |= {r + '1' : [r + '0', 'h' + str(i + 1),'h' + str(i + 2) ] for i, r in enumerate(['a','b','c','d'])}
direct_paths |= {r + '0': [r + '1'] for r in ['a','b','c','d']}
dbg(direct_paths)

@cache
def path(f,t):
    if t in direct_paths[f]:
        return []
    else:
        if f[0]==t[0]=='h':
            visited = set([k+str(i) for k in ['a','b','c','d'] for i in [0,1]])
        else:
            rooms = ['a','b','c','d']
            try:
                rooms.remove(f[0])
            except:
                pass
            try:
                rooms.remove(t[0])
            except:
                pass
            visited = set([k+str(i) for k in rooms for i in [0,1]])
        paths = {f:[]}
        queue = deque([f])
        while True:
            current = queue.popleft()
            if t in direct_paths[current]:
                return paths[current]
            else:
                for p in direct_paths[current]:
                    if p not in visited:
                        path = paths[current].copy()
                        path.append(p)
                        paths[p] = path
                        visited.add(p)
                        queue.append(p)

            
def distance(f,t):
    if f in distances and t in distances[f]:
        return distances[f][t]
    elif t in distances and f in distances[t]:
        return distances[t][f]
    else:
        # these should only be used by the heuristic function
        if f in ['a0','a1']:
            return distances[f]['h2'] + distances[t]['h2']
        if f in ['b0','b1']:
            if t in ['a0','a1']:
                return distances[f]['h2'] + distances[t]['h2']
            else:
                return distances[f]['h3'] + distances[t]['h3']
        if f in ['c0','c1']:
            if t in ['d0','d1']:
                return distances[f]['h4'] + distances[t]['h4']
            else:
                return distances[f]['h3'] + distances[t]['h3']
        if f in ['d0','d1']:
            return distances[f]['h4'] + distances[t]['h4']
        dbg(f"Panic in distance {f},{t}")
        raise NotImplementedError

def cost(f,t,amphipod):
    return costs[amphipod] * distance(f,t)

def filter_dict(d):
    l = []
    for k in d.keys():
        if d[k] is not None:
            l.append(k)
    return l

def filter_dict_none(d):
    l = []
    for k in d.keys():
        if d[k] is None:
            l.append(k)
    return l

def astar(start,goal):
    queue = PriorityQueue()
    sequence = 0
    queue.put((0,sequence, start))
    sequence += 1
    costs = {start: 0}
    path = {start: None}
    while not queue.empty():
        priority, _, current = queue.get()
        if current == goal:
            break
        for next_state, move_cost in next_states(current):
           next_cost = costs[current] + move_cost
           if next_state not in costs or next_cost < costs[next_state]:
               costs[next_state] = next_cost
               priority = next_cost + heuristic(next_state)
               dbg(f"astar add to queue {(priority,next_state)} heuristic {heuristic(next_state)}")
               queue.put((priority,sequence,next_state))
               sequence += 1
               path[next_state] = current
    return path, costs, priority

def intersection(l0,l1):
    return list(set(l0) & set(l1))

def next_states(state):
    froms = filter_dict(state)
    tos = filter_dict_none(state)
    for f in froms:
        a = state[f]
        for t in tos:
            dbg(f"next_states trying {f} -> {t} : {a}")
            if t[0] == 'h' and f[0] == 'h':
                dbg("no hallway to hallway")
                continue # never move from corridor other than to room
            if t[0] != 'h' and state[f].lower() != t[0]:
                dbg("don't move into the wrong room")
                continue # never move into a room unless it's the right room
            if t[0] != 'h' and state[t[0] + '0'] and state[t[0] + '0'] != t[0].upper():
                dbg("bad occupant")
                continue # don't move into the room if the other occupant is the wrong type
            if f[0] != 'h' and f[1]== '0' and state[f] == f[0].upper():
                dbg("leaving right room")
                continue # never leave the correct room
            if f[0] != 'h' and f[1]== '1' and state[f] == f[0].upper() and state[f[0] + '0']== f[0].upper():
                dbg("leaving right room")
                continue # never leave the correct room
            passable = True
            for p in path(f,t):
                if state[p] is not None:
                    dbg(f"cannot pass {p}")
                    passable = False
            if passable:
                new_state = frozendict(state | {f: None, t: a})
                yield new_state, cost(f,t,a)

def heuristic(state):
    """Attempt to move all found amphipods to the correct room, ignoring if it's possible to do so
       Will always be the exact cost or less than the true cost
       First move to the bottom room, then the top"""
    locations = filter_dict(state)
    h = 0
    seen = []
    for l in locations:
        amphipod = state[l]
        if l[0].upper() != amphipod:
            t = amphipod.lower()+'0'
            if state[t] != amphipod and amphipod not in seen:
                h += cost(l,t,amphipod)
                seen.append(amphipod)
            else:
                t = amphipod.lower()+'1'
                h += cost(l,t,amphipod)
    return h

def part1(positions):
    state = frozendict({k: None for k in distances['a0']} | positions)
    goal = frozendict({k: None for k in distances['a0']} | {k: k[0].upper() for k in distances })
    path, costs, prio = astar(state,goal)
    return prio

def part2(positions):
    # add these
    #  a1..d1 remain same
    #  #D#C#B#A# <- new a..d0
    #  #D#B#A#C# < new a..d2
    #  a..d3 <- old d0
    state = frozendict({k: None for k in distances['a0']} | positions)
    goal = frozendict({k: None for k in distances['a0']} | {k: k[0].upper() for k in distances })
    path, costs, prio = astar(state,goal)
    return prio

def parse(lines):
    bottom_buckets = lines[3].split('#')
    top_buckets = lines[2].split('#')
    buckets = [[bottom_buckets[i - 2],top_buckets[i]] for i in range(3,7)]
    return {c+str(j): buckets[i][j] for i,c in enumerate(['a','b','c','d']) for j in range(2)}


if __name__ == '__main__':
    test_infile = sys.argv[0][:-3] + '-test.txt'
    test_data = open(test_infile).read().strip()
    test_lines = [x for x in test_data.split('\n')]
    test_parsed  = parse(test_lines)

    infile = sys.argv[0][:-3] + '-input.txt'
    data = open(infile).read().strip()
    lines = [x for x in data.split('\n')]
    parsed  = parse(lines)
    p1 = part1(test_parsed)
    print("Part 1")
    print("======")
    if p1 == 12521:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 5:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

def test_start():
    positions = {'a0':'A','a1':'B','b0':'D','b1':'C','c0':'C','c1':'B','d0':'A','d1':'D'}
    start = frozendict({k: None for k in distances['a0']} | positions)
    positions = {'a0':'A','a1':'B','b0':'D','b1':'C','c0':'C','c1':None,'d0':'A','d1':'D','h2':'B'}
    first = frozendict({k: None for k in distances['a0']} | positions)
    found = False
    for pos, cost in next_states(start):
        if pos == first:
            assert cost == 40
            found = True
    assert found
    positions = {'a0':'A','a1':'B','b0':'D','b1':None,'c0':'C','c1':'C','d0':'A','d1':'D','h2':'B'}
    second = frozendict({k: None for k in distances['a0']} | positions)
    found = False
    for pos, cost in next_states(first):
        if pos == second:
            assert cost == 400
            found = True
    assert found
    positions = {'a0':'A','a1':'B','b0':None,'b1':None,'c0':'C','c1':'C','d0':'A','d1':'D','h2':'B','h3':'D'}
    third = frozendict({k: None for k in distances['a0']} | positions)
    found = False
    for pos, cost in next_states(second):
        if pos == third:
            assert cost == 3000
            found = True
    assert found
    positions = {'a0':'A','a1':'B','b0':'B','b1':None,'c0':'C','c1':'C','d0':'A','d1':'D','h3':'D'}
    fourth = frozendict({k: None for k in distances['a0']} | positions)
    found = False
    for pos, cost in next_states(third):
        if pos == fourth:
            assert cost == 30
            found = True
    assert found
    positions = {'a0':'A','a1':None,'b0':'B','b1':'B','c0':'C','c1':'C','d0':'A','d1':'D','h3':'D'}
    fifth = frozendict({k: None for k in distances['a0']} | positions)
    found = False
    for pos, cost in next_states(fourth):
        if pos == fifth:
            assert cost == 40
            found = True
    assert found
    positions = {'a0':'A','a1':None,'b0':'B','b1':'B','c0':'C','c1':'C','d0':'A','d1':None,'h3':'D','h4':'D'}
    sixth = frozendict({k: None for k in distances['a0']} | positions)
    found = False
    for pos, cost in next_states(fifth):
        if pos == sixth:
            assert cost == 2000
            found = True
    assert found
    positions = {'a0':'A','a1':None,'b0':'B','b1':'B','c0':'C','c1':'C','d0':None,'d1':None,'h3':'D','h4':'D','h5':'A'}
    seventh = frozendict({k: None for k in distances['a0']} | positions)
    found = False
    for pos, cost in next_states(sixth):
        if pos == seventh:
            assert cost == 3
            found = True
    assert found
