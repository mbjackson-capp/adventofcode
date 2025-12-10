from aocd import get_data
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple
import re
from collections import Counter

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/10

input = get_data(day=10, year=2025)

test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

ON = "#"
OFF = "."


class Machine:
    def __init__(
        self, start_state: List[str], buttons: List[Tuple], joltage_reqs: List[int]
    ):
        self.start_state = start_state
        self.lights = [OFF] * len(self.start_state)
        self.buttons = buttons
        self.joltage_reqs = joltage_reqs

    def __repr__(self):
        return f"Machine(lights={self.lights}, start_state={self.start_state}, buttons={self.buttons}, joltage_reqs={self.joltage_reqs})"


def parse_input(data: str) -> List[Machine]:
    return [parse_machine(row) for row in data.split("\n")]


def parse_machine(row: str) -> Machine:
    """Turn a row of text in machine spec format, e.g.
    '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}'
    into an instance of class Machine."""
    SPLIT_RE = r"(?:(?<=\])\s(?=\()|(?<=\))\s(?=\{))"
    start_str, buttons_str, joltage_str = re.split(SPLIT_RE, row)

    # use [1:-1] string indexing to ignore bracketing symbols
    start_state = [char for char in start_str[1:-1]]
    print(start_state)

    buttons_text = buttons_str.split(" ")
    buttons = []
    for bt in buttons_text:
        button = tuple(int(i) for i in bt[1:-1].split(","))
        buttons.append(button)
    print(buttons)

    joltage = [int(i) for i in joltage_str[1:-1].split(",")]
    print(joltage)

    m = Machine(start_state, buttons, joltage)
    return m


def all_button_sequences(buttons: List[Tuple], n: int) -> List[List[Tuple]]:
    """Generate, recursively and through brute force, all ways in which
    to push n buttons from the provided list of buttons.
    This will explode quickly; if there are b buttons, the resultant
    list will have b^n entries. Intended to be abandoned for a more
    sensible approach later."""
    # TODO: figure out if press order matters
    # if it doesn't, you can reduce to a set of Counters
    if n < 0:
        raise ValueError(f"n must be greater than 0; got {n}")
    elif n == 0:
        return [[]]
    else:
        new_presses = []
        old_presses = all_button_sequences(buttons, n - 1)
        for press_list in old_presses:
            for b in buttons:
                new_list = deepcopy(press_list + [b])
                new_presses.append(new_list)
        return new_presses


# when given a list of button presses,
# create a Counter with the indices as keys, and the number of times each
# key is within a button as values
# for each index in the Counter, turn that index ON if index is odd
# else leave OFF if index is even (assuming all-OFF starting state)

# this hints at how one would speed this up; you're looking for a collection
# of buttons that has an odd number of each ON index and an even number of each
# OFF index

# there should generally be no reason to push the same button twice;
# doing so will cancel its effect


def min_presses_to_activate(m: Machine):
    n = 1  # will start taking forever on real data once n is about 7
    while True:
        print(f" Attempting n={n}")
        all_seqs = all_button_sequences(m.buttons, n)
        print(f"{len(all_seqs)} possible sequences of button presses to consider")
        for seq in all_seqs:
            lights = deepcopy(m.lights)
            c = Counter()
            for button in seq:
                for i in button:
                    c[i] += 1
            for i, val in c.items():
                lights[i] = ON if val % 2 == 1 else OFF
            if lights == m.start_state:
                print(f"Success")
                return n
        n += 1


# Okay, you can change this
# if the sequence -> Counter -> mod 2 -> light flips logic is sound,
# you don't actually have to track how many times each button is pushed
# in each world.
# you only need to return possible end states of the lights after pressing
# each new button.
# this will be a much smaller space
# Per the pigeonhole principle it can never exceed 2^l where l is the
# number of lights
# and if it hits 2^l you can return immediately because the start state
# is guaranteed to be in there


def part1(data: str) -> int:
    total_presses = 0
    m_list = parse_input(data)
    for i, m in enumerate(m_list):
        print(f"Now evaluating machine {i}")
        total_presses += min_presses_to_activate(m)
    return total_presses


if __name__ == "__main__":
    p1_test = part1(test_input)
    print(f"Part 1 test: {p1_test}")
    p1_ans = part1(input)
    print(f"Part 1 answer: {p1_ans}")
