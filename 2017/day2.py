from aocd import get_data
from typing import List
import re


def parse_input(data: str) -> List[List[int]]:
    lines = data.split("\n")
    sheet = []
    for line in lines:
        sheet.append([int(i) for i in re.split(r"\s+", line)])
    return sheet


def largest_smallest_difference(row: List[int]) -> int:
    return max(row) - min(row)


def sheet_sum(sheet: List[List[int]], func):
    return int(sum([func(row) for row in sheet]))


def find_even_dividers(row: List[int]) -> int:
    """Find the two numbers that, when one divides the other, result in
    an integer, then return the result of dividing the larger by the smaller."""
    for i in range(len(row)):
        for j in range(i + 1, len(row)):
            if (row[i] / row[j] == int(row[i] / row[j])) or (
                row[j] / row[i] == int(row[j] / row[i])
            ):
                return max(row[j] / row[i], row[i] / row[j])
    raise ValueError("Somehow, you didn't find two integers that divide each other")


if __name__ == "__main__":
    input = get_data(day=2, year=2017)
    sheet = parse_input(input)
    print(f"Part 1 answer: {sheet_sum(sheet, largest_smallest_difference)}")
    print(f"Part 2 answer: {sheet_sum(sheet, find_even_dividers)}")
