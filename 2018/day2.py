from aocd import get_data
from typing import List
from collections import Counter

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2018/day/2
input = [i for i in get_data(day=2, year=2018).split("\n")]


def has_n_of_a_letter(str, n: int) -> bool:
    ctr = Counter(str)
    return n in ctr.values()


def letters_in_common(id1: str, id2: str) -> str:
    assert len(id1) == len(id2), "ID strings are of different lengths"
    result = ""
    diff_count = 0
    for i in range(len(id1)):
        if id1[i] == id2[i]:
            result += id1[i]
        else:
            diff_count += 1
    return (diff_count == 1), result


def part1(data: List[str]) -> int:
    count2 = 0
    count3 = 0
    for box_id in data:
        if has_n_of_a_letter(box_id, 2):
            count2 += 1
        if has_n_of_a_letter(box_id, 3):
            count3 += 1
    return count2 * count3


def part2(data: List[str]) -> str:
    # TODO: is it possible to beat O(n^2)?
    for i, id1 in enumerate(data):
        for j, id2 in enumerate(data[i + 1 :]):
            is_solution, ans = letters_in_common(id1, id2)
            if is_solution:
                return ans
    return None


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(input)}")
    print(f"Part 2 answer: {part2(input)}")
