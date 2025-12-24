from aocd import get_data
from typing import Optional, List, Tuple
from dataclasses import dataclass
import re

input = get_data(day=23, year=2015)


@dataclass
class Instruction:
    command: str
    register: Optional[str] = None
    offset: Optional[int] = None

    def __repr__(self):
        return (
            f"<{self.command} "
            f"{self.register if self.register is not None else ''} "
            f"{self.offset if self.offset is not None else ''}>"
        )


def parse_instructions(data: str):
    lines = data.split("\n")
    instructions = []
    for line in lines:
        command = line[:3]
        register = "a" if " a" in line else "b" if " b" in line else None
        OFFSET_FIND = re.findall(r"-?\d+", line)
        offset = int(OFFSET_FIND[0]) if OFFSET_FIND else None
        instructions.append(Instruction(command, register, offset))
    return instructions


def execute_all(instructions: List[Instruction], part=1) -> int:
    registers = {"a": 0, "b": 0}
    if part == 2:
        registers["a"] = 1
    pointer = 0
    while pointer < len(instructions):
        registers, pointer = execute(registers, pointer, instructions[pointer])
    return registers["b"]


def execute(
    registers: dict, pointer: int, i: Instruction, debug: bool = False
) -> Tuple[dict, int]:
    if debug:
        print(f"Now executing instruction {i} at index {pointer} on {registers}")
    if i.command == "hlf":  # HALVE
        registers[i.register] //= 2
        pointer += 1
    elif i.command == "tpl":  # TRIPLE
        registers[i.register] *= 3
        pointer += 1
    elif i.command == "inc":  # INCREMENT
        registers[i.register] += 1
        pointer += 1
    elif i.command == "jmp":  # JUMP
        pointer += i.offset
    elif i.command == "jie" and (registers[i.register] % 2 == 0):  # JUMP IF EVEN
        pointer += i.offset
    elif i.command == "jio" and (registers[i.register] == 1):  # JUMP IF ONE
        pointer += i.offset
    else:
        pointer += 1
    if any(v < 0 or v != float(v) for v in registers.values()):
        raise ValueError("Register can only contain non-negative integer values")
    return registers, pointer


if __name__ == "__main__":
    instructions = parse_instructions(input)
    print(f"Part 1 answer: {execute_all(instructions)}")
    print(f"Part 2 answer: {execute_all(instructions, part=2)}")
