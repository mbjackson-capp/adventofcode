from aocd import get_data
import re
import json
from typing import List

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=12, year=2015)


def part1(data: str) -> int:
    """Cheese method to sum up all numeric substrings of arbitrary text input"""
    NUMERIC_RE = r"-?\d+"
    numerics = re.findall(NUMERIC_RE, data)
    if not numerics:
        return 0
    return sum([int(i) for i in numerics])


def part2(obj: dict | int | List | str) -> int:
    if isinstance(obj, str):
        return 0
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, list):
        return sum([part2(i) for i in obj])
    elif isinstance(obj, dict):
        if "red" in obj.keys() or "red" in obj.values():
            return 0
        else:
            return sum([part2(i) for i in obj.values()])


def test_part2():
    answers = [
        ([1, 2, 3], 6),
        ([1, {"c": "red", "b": 2}, 3], 4),
        ({"d": "red", "e": [1, 2, 3, 4], "f": 5}, 0),
        ([1, "red", 5], 6),
    ]
    for pair in answers:
        k, v = pair
        ans = part2(k)
        assert ans == v, f"Expected part2({k}) == {v}, got {ans}"


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(input)}")
    test_part2()
    print(f"Part 2 answer: {part2(json.loads(input))}")
