#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import math

infile = sys.argv[1] if len(sys.argv)>1 else (sys.argv[0][:-3] + '-test.txt')
data = open(infile).read().strip()
lines = [x for x in data.split('\n')]
re_blueprint = re.compile(r"Blueprint (?P<id>[0-9]+): Each ore robot costs (?P<ore_ore>[0-9]+) ore. Each clay robot costs (?P<clay_ore>[0-9]+) ore. Each obsidian robot costs (?P<obsidian_ore>[0-9]+) ore and (?P<obsidian_clay>[0-9]+) clay. Each geode robot costs (?P<geode_ore>[0-9]+) ore and (?P<geode_obsidian>[0-9]+) obsidian.")
blueprints = [re_blueprint.match(line).groupdict() for line in lines]
blueprints = [dict([k, int(v)] for k, v in blueprint.items()) for blueprint in blueprints]

def max_geodes(blueprint, time_r, ore_robots, ore, clay_robots, clay, obsidian_robots, obsidian, geode_robots, geodes):
    if time_r == 0:
        return geodes
    # always build a geode bot if possible

    if ore >= blueprint['geode_ore'] and obsidian >= blueprint['geode_obsidian']:
        geodes_geodes = max_geodes(blueprint, time_r - 1, ore_robots, ore - blueprint['geode_ore'] + ore_robots,clay_robots,clay+clay_robots,obsidian_robots, obsidian_robots + obsidian - blueprint['geode_obsidian'], geode_robots + 1, geodes + geode_robots)
        return geodes_geodes
    geodes_options = []
    if ore >= blueprint['obsidian_ore'] and clay >= blueprint['obsidian_clay'] and obsidian_robots < blueprint['geode_obsidian']:
        geodes_obsidian = max_geodes(blueprint, time_r - 1, ore_robots, ore - blueprint['obsidian_ore'] + ore_robots,clay_robots,clay - blueprint['obsidian_clay'] + clay_robots,obsidian_robots + 1, obsidian_robots + obsidian, geode_robots, geodes + geode_robots)
        if obsidian_robots == 0:
            # always build obsidian robot if we don't have one
            return geodes_obsidian
        geodes_options.append(geodes_obsidian)
    if ore >= blueprint['clay_ore'] and clay_robots < blueprint['obsidian_clay']:
        geodes_clay = max_geodes(blueprint, time_r - 1, ore_robots, ore - blueprint['clay_ore'] + ore_robots,clay_robots + 1,clay+clay_robots,obsidian_robots, obsidian_robots + obsidian, geode_robots, geodes + geode_robots)
        geodes_options.append(geodes_clay)
    geodes_nothing = max_geodes(blueprint, time_r - 1, ore_robots, ore+ore_robots,clay_robots,clay+clay_robots,obsidian_robots, obsidian_robots + obsidian, geode_robots, geodes + geode_robots)
    geodes_options.append(geodes_nothing)
    if ore >= blueprint['ore_ore'] and ore_robots < max(blueprint['ore_ore'], blueprint['clay_ore'], blueprint['obsidian_ore'], blueprint['geode_ore']):
        geodes_ore = max_geodes(blueprint, time_r - 1, ore_robots + 1, ore - blueprint['ore_ore'] + ore_robots, clay_robots, clay+clay_robots,obsidian_robots, obsidian_robots + obsidian, geode_robots, geodes + geode_robots)
        geodes_options.append(geodes_ore)
    return max(geodes_options)

def max_geodes_dfs(blueprint, time_r, ore_robots, ore, clay_robots, clay, obsidian_robots, obsidian, geode_robots, geodes):
    if time_r == 0:
        return geodes
    # if possible, build a geode bot
    geodes_options = []
    if obsidian_robots >= blueprint['geode_obsidian'] and ore_robots >= blueprint['geode_ore']:
        # build a geode robot every time unit remaining
        geodes_geodes  = geodes + geode_robots * time_r + sum(range(time_r))
        geodes_options.append(geodes_geodes)
        return geodes_geodes
    if obsidian_robots > 0:
        target_obsidian = blueprint['geode_obsidian']
        target_ore = blueprint['geode_ore']
        time = max(1 + math.ceil((target_obsidian - obsidian) / obsidian_robots), 1 + math.ceil((target_ore - ore) / ore_robots),1)
        if time <= time_r:
            geodes_geodes = max_geodes_dfs(blueprint, time_r - time, ore_robots, ore + ore_robots * time - target_ore, clay_robots, clay + clay_robots * time, obsidian_robots, obsidian + obsidian_robots * time - target_obsidian, geode_robots + 1, geodes + geode_robots * time)
            geodes_options.append(geodes_geodes)
    # next try an obsidian robot
    if clay_robots > 0 and obsidian_robots < blueprint['geode_obsidian']:
        target_clay = blueprint['obsidian_clay']
        target_ore = blueprint['obsidian_ore']
        time = max(1 + math.ceil((target_clay - clay) / clay_robots), 1 + math.ceil((target_ore - ore) / ore_robots),1)
        if time <= time_r:
            geodes_obsidian = max_geodes_dfs(blueprint, time_r - time, ore_robots, ore + ore_robots * time - target_ore, clay_robots, clay + clay_robots * time - target_clay, obsidian_robots + 1, obsidian + obsidian_robots * time, geode_robots, geodes + geode_robots * time)
            geodes_options.append(geodes_obsidian)
    # next try a clay robot
    if clay_robots < blueprint['obsidian_clay']:
        target_ore = blueprint['clay_ore']
        time = max(1 + math.ceil((target_ore - ore) / ore_robots),1)
        if time <= time_r:
            geodes_clay = max_geodes_dfs(blueprint, time_r - time, ore_robots, ore + ore_robots * time - target_ore, clay_robots + 1, clay + clay_robots * time, obsidian_robots, obsidian + obsidian_robots * time, geode_robots, geodes + geode_robots * time)
            geodes_options.append(geodes_clay)
    if ore_robots < max(blueprint['ore_ore'], blueprint['clay_ore'], blueprint['obsidian_ore'], blueprint['geode_ore']):
        target_ore = blueprint['clay_ore']
        target_ore = blueprint['ore_ore']
        time = max(1 + math.ceil((target_ore - ore) / ore_robots),1)
        if time <= time_r:
            geodes_ore = max_geodes_dfs(blueprint, time_r - time, ore_robots + 1, ore + ore_robots * time - target_ore, clay_robots, clay + clay_robots * time, obsidian_robots, obsidian + obsidian_robots * time, geode_robots, geodes + geode_robots * time)
            geodes_options.append(geodes_ore)
    geodes_nothing = geodes + time_r * geode_robots
    geodes_options.append(geodes_nothing)
    return max(geodes_options)


def part1():
    TIME = 24
    ore_robots = 1
    scores = []
    for bp in blueprints:
        min_ore = min(bp['ore_ore'],bp['clay_ore'])
        max_geode = max_geodes(bp, TIME - min_ore, ore_robots, min_ore, 0, 0, 0, 0, 0, 0)
        max_geode_dfs = max_geodes_dfs(bp, TIME, ore_robots, 0, 0, 0, 0, 0, 0, 0)
        scores.append(max_geode * bp['id'])
        print(f"{bp['id']} min_ore: {min_ore} max_geodes: {max_geode} max_geodes_dfs: {max_geode_dfs} score {scores[-1]}")
    print(sum(scores))

def part2():
    TIME = 32
    ore_robots = 1
    score = 1
    for bp in blueprints[0:3]:
        max_geode = max_geodes_dfs(bp, TIME, ore_robots, 0, 0, 0, 0, 0, 0, 0)
        score = score * max_geode
    print(score)
def test_dfs():
    # start from solution and work backwards
    lines = ['Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.']
    blueprints = [re_blueprint.match(line).groupdict() for line in lines]
    blueprints = [dict([k, int(v)] for k, v in blueprint.items()) for blueprint in blueprints]
    bp = blueprints[0]

    # Minute 32 (time_r = 0)
    assert(56 == max_geodes_dfs(bp,0,2,8,7,84,5,10,9,56))
    # Minute 31 (time_r = 1)
    assert(56 == max_geodes_dfs(bp,1,2,6,7,77,5,5,9,47))
    # Minute 30 (time_r = 2)
    assert(56 == max_geodes_dfs(bp,2,2,6,7,70,5,7,8,39))
    # Minute 20 (time_r = 12)
    assert(56 == max_geodes_dfs(bp,12,2,3,7,14,4,7,1,0))
    # Minute 12 (time_r = 20)
    assert(56 == max_geodes_dfs(bp,20,2,3,6,15,0,0,0,0))
    # Minute 0 (time_r = 32)
    assert(56 == max_geodes_dfs(bp,32,1,0,0,0,0,0,0,0))
#test_dfs()
#part1()
part2()
