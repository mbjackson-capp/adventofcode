from aocd import get_data
from typing import Tuple, List
from math import sqrt, ceil, floor
from utils import manhattan_dist

input = int(get_data(day=3, year=2017))


def layer_bounds(n: int) -> Tuple[int, int]:
    """Given an integer n, obtain the numeric range of the spiral layer of its
    corresponding space in the infinite grid. (Note that each spiral layer has
    an odd square number in its bottom-right position, so the lower bound will
    be the highest odd square number less than n, and the upper bound will be
    the lowest odd square number greater than n.)"""
    lb = floor(sqrt(n)) if floor(sqrt(n)) % 2 == 1 else floor(sqrt(n)) - 1
    ub = ceil(sqrt(n)) if ceil(sqrt(n)) % 2 == 1 else ceil(sqrt(n)) + 1
    return lb**2, ub**2


# there will always be an even number of integers within a layer bound,
# 8, then 16, then 32, then 40, etc.
def quarters(bounds: Tuple[int, int]):
    lb, ub = bounds
    bounds_width = ub - lb
    bin_width = bounds_width // 4

    up_end = lb + bin_width
    left_end = up_end + bin_width
    down_end = left_end + bin_width

    return (
        range(lb + 1, up_end + 1),
        range(up_end + 1, left_end + 1),
        range(left_end + 1, down_end + 1),
        range(down_end, ub + 1),
    )


def layer_corners(layer: int) -> Tuple[Tuple[int, int]]:
    ur = (-layer, layer)
    ul = (-layer, -layer)
    dl = (layer, -layer)
    dr = (layer, layer)
    return ur, ul, dl, dr


def grid_coordinates(n: int) -> Tuple[int, int]:
    """Left coordinate represents vertical row above/below 1,
    right coordinate represents horizontal column right/left of 1"""
    spiral_level = ceil(sqrt(n)) // 2
    if sqrt(n) == int(sqrt(n)) and n % 2 == 1:
        return (spiral_level, spiral_level)

    qtrs = quarters(layer_bounds(n))
    corners = layer_corners(spiral_level)
    for rng, max_loc in list(zip(qtrs, corners))[::-1]:
        max_val = max(list(rng))
        if n not in rng:
            continue
        elif n == max_val:
            return max_loc
        else:  # n > max_val
            x, y = max_loc
            diff = max_val - n
            if max_loc == corners[0]:  # part of spiral layer going up
                return (x + diff, y)
            elif max_loc == corners[1]:  # going left
                return (x, y + diff)
            elif max_loc == corners[2]:  # going down
                return (x - diff, y)
            else:  # going right
                return (x, y - diff)


def part1(n: int) -> int:
    return manhattan_dist(grid_coordinates(n), (0, 0))


def neighbor_locs(loc: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Returns the indices of neighbors of a location in an infinite 2-dimensional
    grid centered on (0,0), including diagonals. Simplifies a function from utils."""
    x, y = loc
    neighbor_locs = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            else:
                this_x = x + dx
                this_y = y + dy
                neighbor_locs.append((this_x, this_y))
    return neighbor_locs


def part2(threshold: int) -> int:
    max_val_seen = 0
    grid = {(0, 0): 1}
    n = 1
    while max_val_seen <= threshold:
        n += 1
        loc = grid_coordinates(n)
        new_entry = sum([grid[nloc] for nloc in neighbor_locs(loc) if nloc in grid])
        grid[loc] = new_entry
        max_val_seen = new_entry
    return max_val_seen


if __name__ == "__main__":
    print(f"Part 1 answer: {part1(input)}")
    print(f"Part 2 answer: {part2(input)}")
