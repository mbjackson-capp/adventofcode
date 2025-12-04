from aocd import get_data
from typing import List

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/3


def bankify(data: str) -> List[List[int]]:
    return [[int(i) for i in bank] for bank in data.split("\n")]


def max_joltage(bank: List[int], size: int = 12) -> str:
    """Obtain the digits of the maximum possible joltage as a string. Recursive."""
    # Base case: all batteries have been evaluated. Return empty string
    if size == 0:
        return ""
    # Recursive step: find the first of the remaining characters
    new_ix = None
    new_digit = 0
    # ignore last 11 characters if there are 12 left to get, e.g.
    # ifelse clause is hacky way to get full list when bank[:0] would be empty;
    # bank[:None] selector gets full list
    last_option = -size + 1 if size > 1 else None
    for i, bat in enumerate(bank[:last_option]):
        if bat > new_digit:
            new_ix = i
            new_digit = bat
            if bat == 9:
                break
    # Put new digit on front, then look only at digits past it when recursing
    return str(new_digit) + max_joltage(bank[new_ix + 1 :], size=size - 1)


def solve(data: str, size=12) -> int:
    banks = bankify(data)
    total_joltage = 0
    for bank in banks:
        total_joltage += int(max_joltage(bank, size=size))
    return total_joltage


if __name__ == "__main__":
    input_data = get_data(day=3, year=2025)
    print(f"Part 1 answer: {solve(input_data, size=2)}")
    print(f"Part 2 answer: {solve(input_data)}")
