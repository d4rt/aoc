#!/usr/bin/env python3

import sys
import re


re_monkey = re.compile(r"Monkey (?P<monkey>[0-9]+):")
re_items = re.compile(r"  Starting items: (?P<items>[0-9 ,]+)" )
re_operation = re.compile(r"  Operation: new = (?P<left>[old0-9]+) (?P<op>[-+*]) (?P<right>[old0-9]+)")
re_test = re.compile(r"  Test: divisible by (?P<divisor>[0-9]+)")
re_action = re.compile(r"    If (?P<cond>true|false): throw to monkey (?P<monkey>[0-9]+)")

monkeys = {}

with open(sys.argv[1]) as infile:
    while(line := infile.readline().rstrip()):
        match = re_monkey.match(line)
        monkey = {"monkey": int(match.group('monkey')) }
        match = re_items.match(infile.readline().rstrip())
        monkey["items"] = [int(i) for i in match.group('items').split(',')]
        match = re_operation.match(infile.readline().rstrip())
        monkey["operation"] = match.groupdict()
        match = re_test.match(infile.readline().rstrip())
        monkey["test"] = int(match.group('divisor'))
        match = re_action.match(infile.readline().rstrip())
        monkey["true"] = int(match.group('monkey'))
        match = re_action.match(infile.readline().rstrip())
        monkey["false"] = int(match.group('monkey'))
        monkey["inspections"] = 0
        monkeys[monkey['monkey']]= monkey
        infile.readline() # read the blank line

def worry(item, monkey):
    op = monkey['operation']
    left = lr(item,op['left'])
    right = lr(item,op['right'])
    if op['op'] == '+':
        return left + right
    if op['op'] == '-':
        return left - right
    if op['op'] == '*':
        return left * right

def lr(item,tok):
    if tok == 'old':
        return item
    else:
        return int(tok)

def test(item, monkey):
    return item % monkey['test'] == 0

def dest(item, monkey):
    if test(item, monkey):
        return monkey['true']
    return monkey['false']

mod = 1
for m in range(len(monkeys)):
    mod = mod * monkeys[m]['test']


for i in range(10000): # 10000 rounds
    for m in range(len(monkeys)):
        for item in monkeys[m]['items']:
            starting_item = item
            item = worry(item,monkeys[m])
            item = item % mod
            dest_monkey = dest(item, monkeys[m])
            monkeys[dest_monkey]['items'].append(item)
        monkeys[m]['inspections'] = monkeys[m]['inspections'] + len(monkeys[m]['items'])
        monkeys[m]['items'] = []

inspections = sorted([monkeys[m]['inspections'] for m in range(len(monkeys))])
monkey_business = inspections[-2] * inspections[-1]
print(monkey_business)
