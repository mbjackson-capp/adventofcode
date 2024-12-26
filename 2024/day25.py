from aocd import get_data
import numpy as np
from utils import gridify

input = get_data(day=25, year=2024)

LOCK_TOP = ["#"] * 5


def parse_input(data: str):
    schematics = data.split("\n\n")
    locks = []
    keys = []
    for schematic in schematics:
        gridmap = gridify(schematic)
        v = compress(gridmap)
        if np.all(gridmap[0] == LOCK_TOP):
            locks.append(v)
        else:
            keys.append(v)
    return locks, keys


def compress(gridmap: np.array) -> list[int]:
    """TODO: replace with numpy built-in functions"""
    numbers = []
    for row in gridmap.T:
        ct = len(np.where(row == "#")[0]) - 1
        numbers.append(ct)
    return numbers


def fit(result: list[int]):
    MATCH_MAX = 5
    if result == []:
        return True
    if result[0] > MATCH_MAX:
        return False
    else:
        return fit(result[1:])


def part1(input):
    total = 0
    locks, keys = parse_input(input)
    for lock in locks:
        for key in keys:
            result = [lock[i] + key[i] for i, v in enumerate(key)]
            total += fit(result)
    return total


if __name__ == "__main__":
    print(f"Part 1 solution: {part1(input)}")
