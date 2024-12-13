import numpy as np


def gridify(mapstr: str, intify=False, pad_char=None) -> np.array:
    """
    Turn text input of a grid into a 2-dimensional numpy array.
    Parameters:
    - mapstr (str): String with \n returns in it, representing a grid as in
    Advent of Code input.
    - intify (bool): convert text representation of digits into integers
    if True, leave as-is otherwise
    - pad_char (int or str or None): what character, if any, to use for
    a width-1 pad of grid, in case it makes calculations at edges easier.
    """
    if intify:
        input_as_list = [[int(char) for char in row] for row in mapstr.split("\n")]
    else:
        input_as_list = [[char for char in row] for row in mapstr.split("\n")]
    grid = np.array(input_as_list)
    if pad_char is not None:
        grid = np.pad(grid, pad_width=1, mode="constant", constant_values=pad_char)
    return grid


def neighbor_locs(arr, x, y, include_diag=False):
    """Returns the indices of neighbors of a location in a 2-dimensional array."""
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


def neighbors(arr, x, y, include_diag=False):
    """Returns the values in neighboring cells within a 2-dimensional array."""
    neighbors = []
    for tuple in neighbor_locs(arr, x, y, include_diag):
        this_x, this_y = tuple
        neighbors.append(arr[this_x][this_y])
    return neighbors
