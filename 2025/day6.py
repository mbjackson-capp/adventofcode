from aocd import get_data
from typing import List
from functools import reduce

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/6

input = get_data(day=6, year=2025)

NOT_FOUND = -1


def prepare_input(data: str) -> List[List[int | str]]:
    """Read in cephalopod equations from data, as a list of lists of: space-padded
    numeric strings followed by a space-padded operator string."""
    rows = data.split("\n")
    right_way = []
    while True:
        if set(rows) == {""}:
            break
        # get the width of the widest number at the start of the rows,
        # then make sure smaller numbers are padded with the proper amount of
        # space on either side to work under cephalopod rules
        space_locs = [s.find(" ") for s in rows]
        width = len(rows[0]) if NOT_FOUND in space_locs else max(space_locs)
        new_values = [s[:width] for s in rows]
        right_way.append(new_values)
        # prune the information we just looked at
        rows = [s[width + 1 :] for s in rows]
    return right_way


def cephalopodify(problem: List[int | str]) -> List[int]:
    problem = list(problem)
    op = problem.pop(-1).strip()
    cephalo_numbers = []
    for i in range(len(problem[0])):
        cephalo_numbers.append("".join([n[i] for n in problem]))
    cephalo_numbers = [int(i.strip()) for i in cephalo_numbers]
    # order doesn't matter for addition / multiplication of positive integers
    return cephalo_numbers, op


def solve(data: str, part=1) -> int:
    grand_total = 0
    problems = prepare_input(data)
    for problem in problems:
        if part == 1:
            numbers = [
                int(i.strip()) if i.strip().isnumeric() else i.strip() for i in problem
            ]
            op = numbers.pop(-1)
        else:
            numbers, op = cephalopodify(problem)
        if op == "+":
            solution = reduce(lambda a, b: a + b, numbers)
        elif op == "*":
            solution = reduce(lambda a, b: a * b, numbers)
        else:
            raise ValueError(f"Math problem should have operation '+' or '*', not {op}")
        grand_total += solution
    return grand_total


if __name__ == "__main__":
    print(f"Part 1 answer: {solve(input)}")
    print(f"Part 2 answer: {solve(input, part=2)}")
