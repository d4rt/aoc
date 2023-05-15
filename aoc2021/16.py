#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
import re
from tqdm import tqdm
import numpy as np
import pytest

from dataclasses import dataclass, field

@dataclass
class Packet:
    """Packet spec"""
    version: int = 0
    type: int = 0
    value: int = 0
    length_type_id: int = 0
    length_bytes: int = 0
    length_sub_packets: int = 0
    subpackets: list['Packet'] = field(default_factory=list)

hex = {'0': [0,0,0,0], '1': [0,0,0,1], '2': [0,0,1,0], '3': [0,0,1,1], '4': [0,1,0,0],
       '5': [0,1,0,1], '6': [0,1,1,0], '7': [0,1,1,1], '8': [1,0,0,0], '9': [1,0,0,1],
       'A': [1,0,1,0], 'B': [1,0,1,1], 'C': [1,1,0,0], 'D': [1,1,0,1], 'E': [1,1,1,0],
       'F': [1,1,1,1]}

def hex_string_to_bit_list(h):
    bits = []
    for c in h:
        bits.extend(hex[c])
    return bits

def bits_to_int(bits):
    int = 0
    for i, b in enumerate(reversed(bits)):
        int += b * (2 ** i)
    return int

def bits_to_binary_string(b):
    pass
def bytes_to_packets(b):
    pass
def sum_versions(packet):
    return packet.version + sum([sum_versions(sp) for sp in packet.subpackets])
def part1(packet):
    return sum_versions(packet)
def part2(packet):
    return eval_packet(packet)

def eval_packet(packet: Packet):
    if packet.type == 4:
        return packet.value
    subpacket = [eval_packet(sp) for sp in packet.subpackets]
    if packet.type == 0:
        return sum(subpacket)
    if packet.type == 1:
        return np.prod(subpacket)
    if packet.type == 2:
        return min(subpacket)
    if packet.type == 3:
        return max(subpacket)
    if packet.type == 5:
        return 1 if subpacket[0] > subpacket[1] else 0
    if packet.type == 6:
        return 1 if subpacket[0] < subpacket[1] else 0
    if packet.type == 7:
        return 1 if subpacket[0] == subpacket[1] else 0


def parse_packet(bits):
    return parse_packet_offset(bits,0)[0]

def parse_packet_offset(bits,offset):
    bits = bits[offset:]
    #print(f"Parsing packet : {''.join(str(bits))}")
    packet = Packet()
    packet.version = bits_to_int(bits[0:3])
    packet.type = bits_to_int(bits[3:6])
    if packet.type == 4:
        # literal
        # read 5 bytes at a time until 0 in first position
        number = []
        offset = 6
        while True:
           five = bits[offset:offset + 5]
           offset += 5
           number.extend(five[1:])
           if five[0] == 0:
               break
        packet.value = bits_to_int(number)
    else:
        # operator
        packet.length_type_id = bits[6]
        if packet.length_type_id == 1:
            # 11 bits, number of packets
            packet.length_sub_packets = bits_to_int(bits[7:18])
            offset = 18
            for p in range(packet.length_sub_packets):
                subpacket, read = parse_packet_offset(bits,offset)
                #print(f"subpacket decoded : {subpacket} read {read} bits")
                packet.subpackets.append(subpacket)
                offset += read
        else:
            packet.length_bytes = bits_to_int(bits[7:22])
            offset = 22
            while offset < 22 + packet.length_bytes:
                subpacket, read = parse_packet_offset(bits,offset)
                packet.subpackets.append(subpacket)
                offset += read
                #print(f"subpacket decoded : {subpacket} read {read} bits new offset {offset} length {packet.length_bytes} comp {22 + packet.length_bytes}")

    return (packet,offset)

def parse(lines):
    bits = hex_string_to_bit_list(lines[0])
    return parse_packet(bits)

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
    if p1 == 31:
        print(p1)
        print(part1(parsed))
    else:
        print(f"failed - {p1}")
    p2 = part2(test_parsed)
    print("Part 2")
    print("======")
    if p2 == 54:
        print(p2)
        print(part2(parsed))
    else:
        print(f"failed - {p2}")

def test_literal_packet():
    assert parse_packet(hex_string_to_bit_list("D2FE28")).value == 2021

def test_operator_packet():
    packet = parse_packet(hex_string_to_bit_list("EE00D40C823060"))
    assert len(packet.subpackets) == 3
    assert packet.version == 7
    assert packet.subpackets[0].value == 1
    assert packet.subpackets[1].value == 2
    assert packet.subpackets[2].value == 3

@pytest.mark.parametrize("packet,sumver",[("8A004A801A8002F478",16),("620080001611562C8802118E34",12),("C0015000016115A2E0802F182340",23)])
def test_more_packets(packet, sumver):
    assert part1(parse(packet)) == sumver
