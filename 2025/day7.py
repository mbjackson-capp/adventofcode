from utils import gridify
from aocd import get_data
from typing import List, Tuple, Set
from collections import Counter

import numpy as np

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/6

input = get_data(day=7, year=2025)


def tuplify(
    arr: np.array, as_set=False
) -> List[Tuple[int, int]] | Set[Tuple[int, int]]:
    """Convert a weird numpy array thing into a list of clean 2-tuples of ints"""
    tuplist = []
    for row in arr:
        tuplist.append((int(row[0]), int(row[1])))
    return set(tuplist) if as_set else tuplist


def prepare(data: str) -> int:
    manifold = gridify(data)
    max_vert = manifold.shape[0]
    start = tuplify(np.argwhere(manifold == "S"))
    splitters = tuplify(np.argwhere(manifold == "^"), as_set=True)
    return start, splitters, max_vert


def descend_p1(beams, splitters) -> Tuple[List[Tuple[int, int]], int]:
    """Helper function for Part 1.
    Simulate the beams going down one unit, splitting anywhere they split.
    Return the new beam locations and the number of times the beam was split"""
    new_beams = set()
    times_split = 0
    for beam in beams:
        space_down = (beam[0] + 1, beam[1])
        if space_down in splitters:
            side_spaces = {(beam[0] + 1, beam[1] - 1), (beam[0] + 1, beam[1] + 1)}
            new_beams = new_beams.union(side_spaces)
            times_split += 1
        else:
            new_beams.add(space_down)
    return list(new_beams), times_split


def descend_p2(histories: Counter, splitters: Set) -> List[List[Tuple[int, int]]]:
    """Helper function for Part 2.
    Inputs:
        - histories (Counter): key is a tuple, value represents how many worlds
        thus far have a path whose endpoint is that tuple.
        - splitters: set of points where splitters are found on the manifold.
    Returns:
        - new_histories (Counter): Looking down a level: key is a tuple, value
        represents how many worlds must have a path whose endpoint is that tuple
        one time-step ahead"""
    new_histories = Counter()
    for beam in histories.keys():
        space_down = (beam[0] + 1, beam[1])
        space_left = (beam[0] + 1, beam[1] - 1)
        space_right = (beam[0] + 1, beam[1] + 1)
        for space in [space_down, space_left, space_right]:
            if space not in new_histories:
                new_histories[space] = 0

        multiplicity = histories[beam]
        if space_down in splitters:
            new_histories[space_left] += multiplicity
            new_histories[space_right] += multiplicity
        else:
            new_histories[space_down] += multiplicity

    return new_histories


def part1(data: str) -> int:
    beams, splitters, max_vert = prepare(data)
    total_times_split = 0
    while beams[0][0] < max_vert:
        beams, ts = descend_p1(beams, splitters)
        total_times_split += ts
    return total_times_split


def part2(data: str) -> int:
    beams, splitters, max_vert = prepare(data)
    histories = Counter(beams)
    level = 0
    while level < max_vert:
        histories = descend_p2(histories, splitters)
        level += 1
    return sum(histories.values())


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(input)}")
    part2(input)
    print(f"Part 2 answer: {part2(input)}")
