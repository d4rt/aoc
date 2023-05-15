#!/usr/bin/env python3
#

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Instruction:
    opcode: int = 99
    c: int = 0
    b: int = 0
    a: int = 0

    def addr(self, machine):
        dest_c = c = machine.memory[machine.pc + 1]
        if self.c == 0:
            c = machine.memory[c]
        if self.c == 2:
            c = machine.memory[c + machine.relative_base]
            dest_c = dest_c + machine.relative_base
        dest_b = b = machine.memory[machine.pc + 2]
        if self.b == 0:
            b = machine.memory[b]
            dest_b = dest_b + machine.relative_base
        if self.b == 2:
            b = machine.memory[b + machine.relative_base]
        dest_a = a = machine.memory[machine.pc + 3]
        if self.a == 0:
            a = machine.memory[a]
        if self.a == 2:
            a = machine.memory[a + machine.relative_base]
            dest_a = dest_a + machine.relative_base
        return c, b, a, dest_c, dest_b, dest_a


opcodes = {
    1: "add",
    2: "mul",
    3: "input",
    4: "output",
    5: "jump-if-true",
    6: "jump-if-false",
    7: "lt",
    8: "eql",
    9: "relative_base",
    99: "exit",
}


def decode_instruction(i: int) -> Instruction:
    op = i % 100
    c = (i % 1000) // 100
    b = (i % 10_000) // 1000
    a = (i % 100_000) // 10_000
    return Instruction(op, c, b, a)


@dataclass
class Intcode:
    memory: defaultdict = field(default_factory=defaultdict(dict))
    pc: int = 0
    debug: bool = False
    stopped: bool = False
    relative_base: int = 0

    @classmethod
    def new(cls, code: list[int], debug=False):
        return Intcode(defaultdict(int, {i: v for i, v in enumerate(code)}))

    def run(self, input=None):
        output = []
        while not self.stopped:
            output.append(self.step(input))
        return output

    def step(self, i: list[int] = None) -> int:
        """Run until output or termination
        Mutates input"""
        debug = self.debug
        bp = False
        while True:
            instruction = decode_instruction(self.memory[self.pc])
            c, b, a, dest_c, dest_b, dest_a = instruction.addr(self)
            if debug:
                dbg = True
                if bp:
                    if eval(bp):
                        dbg= True
                    else:
                        dbg= False
                while dbg:
                    cmd = input(f"{self.pc} : {self.memory[self.pc]} >")
                    if cmd.isnumeric():
                        print(self.memory[int(cmd)])
                    elif cmd == "n" or cmd == "next":
                        dbg = False
                    elif cmd == "r" or cmd == "run":
                        debug = False
                        dbg = False
                    elif cmd[0] == "b":
                        bp = cmd[2:]
                        dbg = False
                    elif cmd[0] == "e":
                        print(eval(cmd[2:]))
                    elif cmd == "i" or cmd == "p":
                        print(instruction)
                        print(f"pc {self.memory[self.pc]}")
                        print(f"instruction {opcodes[instruction.opcode]}")
                        print(f"relative_base {self.relative_base}")
                        print(f"c {dest_c} -> {c}")
                        print(f"b {dest_b} -> {b}")
                        print(f"a {dest_a} -> {a}")

            if instruction.opcode == 1:  # add c b -> dest (a)
                self.memory[dest_a] = c + b
                self.pc += 4
            elif instruction.opcode == 2:  # mul c b -> dest (a)
                self.memory[dest_a] = c * b
                self.pc += 4
            elif instruction.opcode == 3:  # input -> dest (c)
                self.memory[dest_c] = i[0]
                if len(i) > 1:
                    i = i[1:]
                else:
                    i = []
                self.pc += 2
            elif instruction.opcode == 4:  # output c
                self.pc += 2  # increment pc first
                return c
            elif instruction.opcode == 5:  # jump if true (c)
                if c != 0:
                    self.pc = b
                else:
                    self.pc += 3
            elif instruction.opcode == 6:  # jump if false (c)
                if c == 0:
                    self.pc = b
                else:
                    self.pc += 3
            elif instruction.opcode == 7:  # less than
                self.memory[dest_a] = 1 if c < b else 0
                self.pc += 4
            elif instruction.opcode == 8:  # equals
                self.memory[dest_a] = 1 if c == b else 0
                self.pc += 4
            elif instruction.opcode == 9: # adjust relative base
                self.relative_base += c
                self.pc += 2
            elif instruction.opcode == 99:  # exit and return address 0
                self.stopped = True
                return self.memory[0]


def parse(lines: list[str]) -> list[int]:
    return [int(x) for x in lines[0].split(",")]


def run(instructions: list[int], intcode_input=None, debug=False):
    machine = Intcode.new(instructions)
    machine.debug = debug
    return machine.run(input=intcode_input)


def test_decode():
    ins = decode_instruction(1002)
    assert ins.opcode == 2
    assert ins.c == 0
    assert ins.b == 1
    assert ins.a == 0


def test_conditionals():
    equal8 = parse(["3,9,8,9,10,9,4,9,99,-1,8"])
    assert run(equal8, intcode_input=[8])[0] == 1
    assert run(equal8, intcode_input=[9])[0] == 0
    assert run(equal8, intcode_input=[7])[0] == 0
    lt8 = parse(["3,9,7,9,10,9,4,9,99,-1,8"])
    assert run(lt8, intcode_input=[8])[0] == 0
    assert run(lt8, intcode_input=[9])[0] == 0
    assert run(lt8, intcode_input=[7])[0] == 1
    iequal8 = parse(["3,3,1108,-1,8,3,4,3,99"])
    assert run(iequal8, intcode_input=[8])[0] == 1
    assert run(iequal8, intcode_input=[9])[0] == 0
    assert run(iequal8, intcode_input=[7])[0] == 0
    ilt8 = parse(["3,3,1107,-1,8,3,4,3,99"])
    assert run(ilt8, intcode_input=[8])[0] == 0
    assert run(ilt8, intcode_input=[9])[0] == 0
    assert run(ilt8, intcode_input=[7])[0] == 1

def test_relative_base():
    quine = parse(["109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"])
    assert run(quine)[:-1] == quine
    large = parse(["104,1125899906842624,99"])
    assert run(large)[0] == 1125899906842624
    sixteen = parse(["1102,34915192,34915192,7,4,7,99,0"])
    assert len(str(run(sixteen)[0])) == 16
