from aocd import get_data
import re

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2016/day/3

input = [
    [int(num) for num in re.findall(r"\d+", line)]
    for line in get_data(day=3, year=2016).split("\n")
]


def meets_triangle_inequality(a: int, b: int, c: int):
    return a < (b + c)


def count_valid_triangles(input):
    count = 0
    for trio in input:
        a, b, c = trio
        if (
            meets_triangle_inequality(a, b, c)
            and meets_triangle_inequality(b, c, a)
            and meets_triangle_inequality(c, a, b)
        ):
            count += 1
    return count


def make_vertical(processed_input):
    reordered = (
        [i[0] for i in processed_input]
        + [i[1] for i in processed_input]
        + [i[2] for i in processed_input]
    )
    trying_this = [
        # TODO: make more pythonic with itertools
        [reordered[i], reordered[i + 1], reordered[i + 2]]
        for i in range(0, len(reordered), 3)
    ]
    return trying_this


if __name__ == "__main__":
    part1 = count_valid_triangles(input)
    print(f"Part 1 solution: {part1}")
    part2 = count_valid_triangles(make_vertical(input))
    print(f"Part 2 solution: {part2}")
