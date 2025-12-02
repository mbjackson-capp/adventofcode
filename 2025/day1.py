from aocd import get_data
from typing import List

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/1

input = get_data(day=1, year=2025).split("\n")


def get_password(input: List[str], dial: int = 50) -> int:
    p1_ans = 0
    p2_ans = 0
    DIAL_SIZE = 100
    for instruction in input:
        dir = instruction[0]
        clicks = int(instruction[1:])

        endpoint = dial
        for _ in range(clicks):
            if dir == "L":
                endpoint -= 1
            elif dir == "R":
                endpoint += 1
            if endpoint % DIAL_SIZE == 0:
                p2_ans += 1

        dial = endpoint % DIAL_SIZE
        if dial == 0:
            p1_ans += 1
    return p1_ans, p2_ans


if __name__ == "__main__":
    ans_p1, ans_p2 = get_password(input)
    print(f"Part 1 answer: {ans_p1}\nPart 2 answer: {ans_p2}")
