from aocd import get_data
from collections import Counter
import numpy as np
from typing import List, Tuple
from utils import gridify, neighbors


# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/4

input = gridify(get_data(day=4, year=2025))

ROLL = "@"
BLANK = "."


def gettable_rolls(arr: np.array) -> int:
    x_max = len(arr)
    y_max = len(arr[0])
    spots = set()
    for x in range(x_max):
        for y in range(y_max):
            nbrs = Counter(neighbors(arr, x, y, include_diag=True))
            if nbrs[ROLL] < 4 and arr[x][y] == ROLL:
                spots.add((x, y))
    return spots


def remove_rolls(arr: np.array, spots: List[Tuple[int, int]]) -> np.array:
    for spot in spots:
        x, y = spot
        arr[x][y] = BLANK
    return arr


def part2(arr: np.array) -> int:
    score = 0
    while True:
        gettable_spots = gettable_rolls(arr)
        if not gettable_spots:
            break
        score += len(gettable_spots)
        arr = remove_rolls(arr, gettable_spots)
    return score


if __name__ == "__main__":
    p1_ans = len(gettable_rolls(input))
    print(f"Part 1 answer: {p1_ans}")
    p2_ans = part2(input)
    print(f"Part 2 answer: {p2_ans}")
