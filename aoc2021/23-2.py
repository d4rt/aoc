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
costs = {'A': 1, 'B':10, 'C':100, 'D':1000}
distances = {'a3': {'h0':  3, 'h1': 2, 'h2': 2, 'h3': 4, 'h4': 6, 'h5': 8, 'h6': 9},
             'b3': {'h0':  5, 'h1': 4, 'h2': 2, 'h3': 2, 'h4': 4, 'h5': 6, 'h6': 7},
             'c3': {'h0':  7, 'h1': 6, 'h2': 4, 'h3': 2, 'h4': 2, 'h5': 4, 'h6': 5},
             'd3': {'h0':  9, 'h1': 8, 'h2': 6, 'h3': 4, 'h4': 2, 'h5': 2, 'h6': 3}}
ddx = {}
for x in [0,1,2]:
    add = 3-x
    dx = {p[0] + str(x): {k : v + add for k, v in distances[p].items()} for p in distances }
    ddx |= dx
distances |= ddx
direct_paths = {'h0': ['h1'],
                'h1': ['h0','h2','a3'],
                'h2': ['h1','h3','a3','b3'],
                'h3': ['h2','h4','b3','c3'],
                'h4': ['h3','h5','c3','d3'],
                'h5': ['h4','h6','d3'],
                'h6': ['h5']}
direct_paths |= {r + '3' : [r + '2', 'h' + str(i + 1),'h' + str(i + 2) ] for i, r in enumerate(['a','b','c','d'])}
direct_paths |= {r + '2': [r + '1', r + '3'] for r in ['a','b','c','d']}
direct_paths |= {r + '1': [r + '0', r + '2'] for r in ['a','b','c','d']}
direct_paths |= {r + '0': [r + '1'] for r in ['a','b','c','d']}
print(direct_paths)

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
        if f[0] == 'a':
            return distances[f]['h2'] + distances[t]['h2']
        if f[0] == 'b':
            if t[0] == 'a':
                return distances[f]['h2'] + distances[t]['h2']
            else:
                return distances[f]['h3'] + distances[t]['h3']
        if f[0] == 'c':
            if t[0] == 'd':
                return distances[f]['h4'] + distances[t]['h4']
            else:
                return distances[f]['h3'] + distances[t]['h3']
        if f[0] == 'd':
            return distances[f]['h4'] + distances[t]['h4']
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
               queue.put((priority,sequence,next_state))
               sequence += 1
               path[next_state] = current
    return path, costs, priority

def intersection(l0,l1):
    return list(set(l0) & set(l1))

def filter_to_rooms(state,tos,amphipod):
    amphipod_rooms = [amphipod.lower() + str(i) for i in range(4)]
    valid_rooms = [h for h in tos if h[0] == 'h']
    if all([state[room] == None or state[room] == amphipod for room in amphipod_rooms]):
        # return the highest available room (ie. a0 if all empty)
        for r in amphipod_rooms:
            if state[r] == None:
                valid_rooms.append(r)
                break
    return valid_rooms

def filter_froms(state):
    froms = filter_dict(state)
    # any hallway
    valid_rooms = [h for h in froms if h[0] == 'h']
    # only the topmost empty room
    for r in "abcd":
        for i in range(3,-1,-1):
            if state[r+str(i)] is not None:
                valid_rooms.append(r+str(i))
                break
    return valid_rooms

    

def next_states(state):
    froms = filter_froms(state)
    tos = filter_dict_none(state)
    for f in froms:
        a = state[f]
        filtered_tos = filter_to_rooms(state,tos,a)
        for t in filtered_tos:
            if t[0] == 'h' and f[0] == 'h':
                continue # never move from corridor other than to room
            passable = True
            for p in path(f,t):
                if state[p] is not None:
                    passable = False
                    break
            if passable:
                new_state = frozendict(state | {f: None, t: a})
                yield new_state, cost(f,t,a)

def heuristic(state):
    """Attempt to move all found amphipods to the correct room, ignoring if it's possible to do so
       Will always be the exact cost or less than the true cost"""
    locations = filter_dict(state)
    h = 0
    for f in locations:
        a = state[f]
        if a.lower() != f[0]:
            h += cost(f,a.lower()+ '3',a)
    return h

def part1(positions):
    state = frozendict({k: None for k in distances['a0']} | positions)
    goal = frozendict({k: None for k in distances['a0']} | {k: k[0].upper() for k in distances })
    path, costs, prio = astar(state,goal)
    return prio

def part2(positions):
    # add these
    #  a..d3 < - old a..d1
    #  #D#C#B#A# <- new a..d2
    #  #D#B#A#C# < new a..d1
    #  a..d0 <- remain same

    positions = positions | {'a1': 'D', 'a2': 'D', 'b1': 'B', 'b2': 'C', 'c1': 'A', 'c2': 'B', 'd1': 'C', 'd2':'A'}
    state = frozendict({k: None for k in distances['a0']} | positions)
    print(state)
    goal = frozendict({k: None for k in distances['a0']} | {k: k[0].upper() for k in distances })
    path, costs, prio = astar(state,goal)
    return prio


def parse_example(e):
    a = {'A': 'A','B':'B','C': 'C', 'D':'D','.':None}
    lines = e.split('\n')
    positions = {'h'+str(i): a[lines[1][j]] for i,j in [(0,1),(1,2),(2,4),(3,6),(4,8),(5,10),(6,11)]}
    positions |= {r + '3': a[lines[2][(i*2)+3]] for i,r in enumerate(['a','b','c','d'])}
    positions |= {r + '2': a[lines[3][(i*2)+3]] for i,r in enumerate(['a','b','c','d'])}
    positions |= {r + '1': a[lines[4][(i*2)+3]] for i,r in enumerate(['a','b','c','d'])}
    positions |= {r + '0': a[lines[5][(i*2)+3]] for i,r in enumerate(['a','b','c','d'])}
    return frozendict(positions)

if __name__ == '__main__':
    test_parsed  = parse_example("""#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########""")

    parsed  = parse_example("""#############
#...........#
###C#A#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #D#C#A#B#
  #########""")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 44169:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

example ="""#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A..D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...D.....AD#
###.#B#C#.###
  #A#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""

def test_example():
    # check that next_states finds these states, total cost 44619
    states_text = example.split('\n\n')
    assert len(states_text) == 24
    example_steps = [parse_example(s) for s in states_text]
    cost = 0
    for c,n in zip(example_steps[:-1],example_steps[1:]):
        found = False
        for nn, nc in next_states(c):
            if nn == n:
                found = True
                cost += nc
        if not found:
            ns = set(n.items())
            cs = set(c.items())
            print(f"could not find : {ns - cs}  {n} from {c}")
        h = heuristic(c)
        hn = heuristic(n)
        print(f"heuristic {hn}")
        assert hn <= (44169 - cost)
        assert found
    assert cost==44169
