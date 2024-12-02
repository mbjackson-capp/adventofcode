from aocd import get_data
from copy import deepcopy

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2024/day/2

input = get_data(day=2, year=2024).split("\n")
input = [i.split(" ") for i in input]
input = [[int(i) for i in line] for line in input]

MIN_SAFE_DIFF = 1
MAX_SAFE_DIFF = 3


def is_safe(report: list[int]):
    changes = [report[i] - report[i - 1] for i in range(1, len(report))]
    if not is_monotonic(changes):
        return False
    abs_changes = [abs(change) for change in changes]
    if max(abs_changes) > MAX_SAFE_DIFF:
        return False
    return True


def is_monotonic(changes: list[int]) -> bool:
    if any(x == 0 for x in changes):
        return False
    has_increase = any(x > 0 for x in changes)
    has_decrease = any(x < 0 for x in changes)
    return has_increase ^ has_decrease


def part1():
    count_safe = 0
    for report in input:
        count_safe += is_safe(report)
    return count_safe


def part2():
    count_safe = 0
    for report in input:
        if is_safe(report):
            count_safe += 1
            continue
        else:
            for ix, _ in enumerate(report):
                dampened_report = deepcopy(report)
                dampened_report.pop(ix)
                if is_safe(dampened_report):
                    count_safe += 1
                    break
    return count_safe


if __name__ == "__main__":
    print(f"Part 1 solution: {part1()}")
    print(f"Part 2 solution: {part2()}")
