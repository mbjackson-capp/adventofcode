from aocd import get_data
import re

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2024/day/3

input = get_data(day=3, year=2024)

PART1_RE = r"mul\(\d+,\d+\)"
PART2_RE = r"(mul\(\d+,\d+\)|do\(\)|don't\(\))"


def do_mul(mul_string: str) -> int:
    if len(re.findall(PART1_RE, mul_string)) != 1:
        raise ValueError(f"mul-string {mul_string} is improperly formatted")
    mul_args = re.findall(r"\d+", mul_string)
    arg_a = int(mul_args[0])
    arg_b = int(mul_args[1])
    return arg_a * arg_b


def part1():
    total = 0
    muls = re.findall(PART1_RE, input)
    for mul_str in muls:
        total += do_mul(mul_str)
    return total


def part2():
    total = 0
    enabled = True
    commands = re.findall(PART2_RE, input)
    for command in commands:
        if command == "do()":
            enabled = True
        elif command == "don't()":
            enabled = False
        elif enabled:
            total += do_mul(command)
    return total


if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
