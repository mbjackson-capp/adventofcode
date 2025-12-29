from aocd import get_data
from typing import List

input = get_data(day=5, year=2017)


def parse_data(data: str) -> List[int]:
    return [int(i) for i in data.split("\n")]


def steps_to_exit(jumps: List[int], part=1) -> int:
    spot = 0
    n_steps = 0
    while 0 <= spot <= len(jumps):
        try:
            # take the jump
            old_spot = spot
            offset = jumps[spot]
            spot += offset
            n_steps += 1
            # change the spot jumped from
            change = -1 if (part == 2 and offset >= 3) else 1
            jumps[old_spot] += change
        except IndexError:
            break
    return n_steps


if __name__ == "__main__":
    print(f"Part 1 answer: {steps_to_exit(parse_data(input))}")
    print(f"Part 2 answer: {steps_to_exit(parse_data(input), part=2)}")
