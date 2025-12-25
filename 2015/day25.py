from aocd import get_data
import re
from typing import Tuple
from math import sqrt, floor, ceil
from tqdm import tqdm
import time

START_CODE = 20151125
MULTIPLICAND = 252533
MODULUS = 33554393

scrap = """   |    1         2         3         4         5         6
---+---------+---------+---------+---------+---------+---------+
 1 | 20151125  18749137  17289845  30943339  10071777  33511524
 2 | 31916031  21629792  16929656   7726640  15514188   4041754
 3 | 16080970   8057251   1601130   7981243  11661866  16474243
 4 | 24592653  32451966  21345942   9380097  10600672  31527494
 5 |    77061  17552253  28094349   6899651   9250759  31663883
 6 | 33071741   6796745  25397450  24659492   1534922  27995004"""


def make_paper(scrap: str) -> dict:
    paper = {}
    for i, row in enumerate(scrap.split("\n")):
        if i < 2:
            continue
        for j, val in enumerate(re.findall(r"\d+", row)):
            if j == 0:
                continue
            paper[(i - 1, j)] = int(val)
    return paper


def nth_triangular(n: int) -> int:
    return (n * (n + 1)) // 2


def linearize(paper_loc: Tuple[int, int]) -> int:
    """The 2-dimensional coordinates on the paper exist in 1-to-1 correspondence
    with the natural numbers. Given the provided pattern in which the coordinates
    on the paper are filled, return the ordinal number n representing that this
    coordinate is the nth to be filled."""
    row, col = paper_loc
    # each diagonal going up and to the right is like a row of point triangle
    triangle_row = row + col - 1
    return nth_triangular(triangle_row - 1) + col


def coordinatize(n: int) -> Tuple[int, int]:
    """Convert an integer representing the nth coordinate to be filled into the
    actual coordinate to fill on the paper. Undoes linearize()."""
    # Inverse obtained by quadratic formula (considering only the + case since
    # function is applied only to positive integers)
    triangle_row = (-1 + sqrt(8 * n + 1)) / 2
    if triangle_row == floor(triangle_row):
        return (1, int(triangle_row))
    else:
        t_row_min = nth_triangular(floor(triangle_row))
        t_row_max = nth_triangular(ceil(triangle_row))
        row = t_row_max - n + 1
        col = -t_row_min + n
        return (row, col)


target = tuple(int(i) for i in re.findall(r"\d+", get_data(day=25, year=2015)))
assert coordinatize(linearize(target)) == target


def part1():
    reference_paper = make_paper(scrap)
    paper = make_paper(scrap)
    target_ix = linearize(target)
    # TODO: we could add cycle detection to skip to the end faster. But with
    # my input the first potential cycle appears around entry 16_000_000 out of
    # 18_331_560 required to calculate; not super worth it. Pseudoish-code guide
    # to how cycle detection would work included as comments.
    # seen = {}
    for i in tqdm(range(1, target_ix + 1)):
        if i == 22 and reference_paper != paper:
            raise ValueError
        if i == 1:
            paper[(1, 1)] = START_CODE
            # seen[START_CODE] = 1
            continue
        else:
            start = paper[coordinatize(i - 1)]
            new_prod = start * MULTIPLICAND
            new_code = new_prod % MODULUS
            paper[coordinatize(i)] = new_code
            # if new_code in seen:
            #     return value recorded at index target_ix - i + 1
            # seen[new_code] = i
    return paper[target]


if __name__ == "__main__":
    print(f"Part 1 answer: {part1()}")
