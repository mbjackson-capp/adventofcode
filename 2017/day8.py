from aocd import get_data
from typing import List, Tuple

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=8, year=2017).split("\n")

INCREASE = "inc"
DECREASE = "dec"


def satisfies_comparison(amt_1, operator, amt_2) -> bool:
    # TODO: is there a way to literal_eval the comparator out of the string
    # and have it operate on the amounts directly, to reduce branching ifs?
    if operator == "!=":
        return amt_1 != amt_2
    elif operator == "==":
        return amt_1 == amt_2
    elif operator == ">=":
        return amt_1 >= amt_2
    elif operator == "<=":
        return amt_1 <= amt_2
    elif operator == ">":
        return amt_1 > amt_2
    elif operator == "<":
        return amt_1 < amt_2


def run_instructions(data: List[str]) -> Tuple[int, int]:
    registers = {}
    highest_ever_held = 0
    for line in data:
        op_reg, op, op_amt, _, comp_reg, comparator, comp_amt = line.split(" ")
        op_amt = int(op_amt)
        comp_amt = int(comp_amt)
        if op_reg not in registers:
            registers[op_reg] = 0
        if comp_reg not in registers:
            registers[comp_reg] = 0

        if satisfies_comparison(registers[comp_reg], comparator, comp_amt):
            if op == INCREASE:
                registers[op_reg] += op_amt
            elif op == DECREASE:
                registers[op_reg] -= op_amt
        if max(registers.values()) > highest_ever_held:
            highest_ever_held = max(registers.values())
    return max(registers.values()), highest_ever_held


if __name__ == "__main__":
    p1_ans, p2_ans = run_instructions(input)
    print(f"Part 1 answer: {p1_ans}")
    print(f"Part 2 answer: {p2_ans}")
