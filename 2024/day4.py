from aocd import get_data
import numpy as np
from collections import Counter

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
# Problem statement: https://adventofcode.com/2024/day/4

input = get_data(day=4, year=2024).split("\n")
input = np.array([[char for char in row] for row in input])


def neighbor_locs(arr, x, y, include_diag=True):
    """Returns the indices of neighbors of a location in a square array.
    Reused with modifications from my 2021 Day 9."""
    neighbor_locs = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            if not include_diag and dx != 0 and dy != 0:
                continue
            else:
                this_x = x + dx
                this_y = y + dy
                if (
                    this_x >= 0
                    and this_y >= 0
                    and this_x < len(arr)
                    and this_y < len(arr[0])
                ):
                    neighbor_locs.append((this_x, this_y))
    return neighbor_locs


def diags(arr, x, y):
    """Returns all indices diagonal to (i.e. one step vertical and one step horizontal from)
    a starting location within an array, provided that such indices don't exceed array bounds.
    """
    return [loc for loc in neighbor_locs(arr, x, y) if loc[0] != x and loc[1] != y]


def count_xmases(arr, spot: tuple[int, int]) -> int:
    """Count the number of times from which the word 'XMAS' can be spelled from
    the current spot within an array, looking outward in any direction (including
    diagonals.)"""
    x_max = len(arr)
    y_max = len(arr[0])
    x, y = spot
    if arr[x][y] != "X":
        return 0

    m_spots = [loc for loc in neighbor_locs(arr, x, y) if arr[loc[0]][loc[1]] == "M"]
    dirs = [(loc[0] - x, loc[1] - y) for loc in m_spots]

    a_spots = []
    keep_going = []
    for ix, m_spot in enumerate(m_spots):
        x_m, y_m = m_spot
        dx, dy = dirs[ix]
        spot_ahead = (x_m + dx, y_m + dy)
        x_new, y_new = spot_ahead
        if (0 <= x_new < x_max) and (0 <= y_new < y_max) and arr[x_new][y_new] == "A":
            a_spots.append(spot_ahead)
            keep_going.append(ix)
    dirs = [dirs[ix] for ix in keep_going]

    s_spots = []
    for ix, a_spot in enumerate(a_spots):
        x_a, y_a = a_spot
        dx, dy = dirs[ix]
        spot_ahead = (x_a + dx, y_a + dy)
        x_new, y_new = spot_ahead
        if (0 <= x_new < x_max) and (0 <= y_new < y_max) and arr[x_new][y_new] == "S":
            # you found a complete XMAS
            s_spots.append(spot_ahead)
    return len(s_spots)


def part1(arr):
    count = 0
    for i, row in enumerate(arr):
        for j, _ in enumerate(row):
            count += count_xmases(arr, (i, j))
    return count


def part2(arr):
    """Count the number of 'X-MAS'es, i.e. X-shapes where the center is an A
    and both diagonals spell 'MAS' in some direction, within an array."""
    count = 0
    for i, row in enumerate(arr):
        for j, _ in enumerate(row):
            if arr[i][j] != "A":
                continue
            diag_spots = diags(arr, i, j)
            diag_vals = [str(arr[spot[0]][spot[1]]) for spot in diag_spots]
            if Counter(diag_vals) != {"M": 2, "S": 2}:
                continue
            ul, ur, ll, lr = diag_vals
            if ul != lr and ur != ll:  # diagonals cannot read 'SAS' or 'MAM'
                count += 1
    return count


if __name__ == "__main__":
    part1_solution = part1(input)
    print(f"Part 1 solution: {part1_solution}")

    part2_solution = part2(input)
    print(f"Part 2 solution: {part2_solution}")
