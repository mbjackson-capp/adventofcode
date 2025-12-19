from aocd import get_data
import numpy as np
from copy import deepcopy
from utils import gridify, neighbors
from tqdm import tqdm
from typing import List, Tuple

input = get_data(day=18, year=2015)


ON = "#"
OFF = "."


def num_active_neighbors(arr, x, y) -> int:
    nbrs = neighbors(arr, x, y, include_diag=True)
    return len([nbr for nbr in nbrs if nbr == ON])


def tile_next_round(arr, x, y) -> str:
    cur_state = arr[x][y]
    if cur_state == ON:
        return ON if num_active_neighbors(arr, x, y) in (2, 3) else OFF
    elif cur_state == OFF:
        return ON if num_active_neighbors(arr, x, y) == 3 else OFF
    else:
        raise ValueError(
            f"Current state of array[x][y] must be active {ON} or inactive {OFF}"
        )


def next_round(arr: np.array) -> np.array:
    max_x, max_y = arr.shape
    next_arr = deepcopy(arr)
    # TODO: this in a less loopy manner
    for x in range(max_x):
        for y in range(max_y):
            next_arr[x][y] = tile_next_round(arr, x, y)
    return next_arr


def four_corners(arr: np.array) -> List[Tuple]:
    max_x, max_y = arr.shape
    return [(0, 0), (max_x - 1, 0), (0, max_y - 1), (max_x - 1, max_y - 1)]


def light_four_corners(arr: np.array) -> np.array:
    for corner in four_corners(arr):
        x_c, y_c = corner
        arr[x_c][y_c] = ON
    return arr


def solve(data: str, rounds: int = 100, part=1) -> int:
    arr = gridify(data)
    if part == 2:
        arr = light_four_corners(arr)
    for _ in tqdm(range(rounds)):
        arr = next_round(arr)
        if part == 2:
            arr = light_four_corners(arr)
    active_tiles = len(np.argwhere(arr == ON))
    return active_tiles


if __name__ == "__main__":
    print(f"Part 1 answer: {solve(input)}")
    print(f"Part 2 answer: {solve(input, part=2)}")
