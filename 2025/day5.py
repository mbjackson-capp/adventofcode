from aocd import get_data
from typing import Tuple, List, Set

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/5

input = get_data(day=5, year=2025)


def prepare_data(data: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    ranges, ids = data.split("\n\n")
    ranges = [tuple(int(i) for i in i.split("-")) for i in ranges.split("\n")]
    ids = [int(i) for i in ids.split("\n")]
    return ranges, ids


def get_fresh_ids(
    ranges: List[Tuple[int, int]], ids: List[int]
) -> Tuple[Set[int], Set[int]]:
    fresh_ids = set()
    for id in ids:
        added = False
        for rng in ranges:
            if id >= rng[0] and id <= rng[1]:
                fresh_ids.add(id)
                added = True
                continue
            if added:
                break
    return fresh_ids


def part1(data: str) -> int:
    ranges, ids = prepare_data(data)
    return len(get_fresh_ids(ranges, ids))


def have_overlap(rang1: Tuple[int, int], rang2: Tuple[int, int]) -> bool:
    """Check if two numeric ranges have overlap, inclusive of endpoints."""
    lb1, ub1 = rang1
    lb2, ub2 = rang2
    if lb1 > lb2:
        return have_overlap(rang2, rang1)
    return lb2 <= ub1


def condense_ranges(rngs: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Condense a collection of potentially overlapping integer ranges, each
    represented by a tuple of the start and end (inclusive) of that range,
    such that all overlapping ranges are merged.
    Returns all the condensed non-overlapping ranges as an unordered set of
    tuples.
    Example: [(3, 5), (10, 14), (12, 18), (16, 20)] -> {(3, 5), (10, 20)}"""
    result_set = set()
    to_remove = set()
    while rngs:
        new_rng = rngs.pop(0)
        if not result_set:
            result_set.add(new_rng)
            continue
        for result in result_set:
            if have_overlap(new_rng, result):
                to_remove.add(result)
        result_set = result_set - to_remove
        to_add = (
            min([i[0] for i in to_remove] + [new_rng[0]]),
            max([i[1] for i in to_remove] + [new_rng[1]]),
        )
        result_set.add(to_add)
        to_remove = set()
    return result_set


def part2(data: str) -> int:
    total_fresh_ids = 0
    fresh_ranges, _ = prepare_data(data)
    condensed = condense_ranges(fresh_ranges)
    for rng in condensed:
        bottom, top = rng
        total_fresh_ids += top - bottom + 1
    return total_fresh_ids


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(input)}")
    print(f"Part 2 answer: {part2(input)}")
