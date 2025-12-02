from aocd import get_data
from itertools import batched
from typing import List, Tuple

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/2


def get_ranges(input: str) -> List[Tuple[int, int]]:
    input = input.split(",")
    input = [i.split("-") for i in input]
    input = [(int(i[0]), int(i[1])) for i in input]
    return input


def is_valid(int, part=1) -> bool:
    strint = str(int)
    if part == 1 and len(strint) % 2 != 0:
        return True
    halfway = len(strint) // 2
    rmin = halfway if part == 1 else 1
    for i in range(rmin, halfway + 1):
        batches = set(batched(strint, i))
        if len(batches) == 1:  # entire integer is repetitions of same batch
            return False
    return True


def get_all_invalids(id_range: Tuple[int, int], part=1) -> List[int]:
    rmin = min(id_range)
    rmax = max(id_range)
    return [id for id in range(rmin, rmax + 1) if not is_valid(id, part=part)]


def sum_invalid_ids(input: List[Tuple[int, int]], part=1) -> int:
    total_sum = 0
    for id_range in input:
        invalid_id_sum = sum(get_all_invalids(id_range, part=part))
        total_sum += invalid_id_sum
    return total_sum


if __name__ == "__main__":
    input = get_ranges(get_data(day=2, year=2025))
    ans_1 = sum_invalid_ids(input, part=1)
    print(f"Part 1 answer: {ans_1}")
    ans_2 = sum_invalid_ids(input, part=2)
    print(f"Part 2 answer: {ans_2}")
