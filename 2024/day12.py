from aocd import get_data
import numpy as np
from itertools import groupby


def gridify(mapstr: str, intify=False, pad_char=None) -> np.array:
    """Turn text input of a grid into a numpy array. New parameters:
    - intify (bool): convert text representation of digits into integers
    if True, leave as-is otherwise
    - pad_char (int or str or None): what character, if any, to use for
    a width-1 pad of grid, in case it makes calculations at edges easier."""
    # In this problem, padding the grid with "fake" spaces, i.e. neighbors that
    # always fail the "of the same letter" check, helps properly count perimeter.
    if intify:
        input_as_list = [[int(char) for char in row] for row in mapstr.split("\n")]
    else:
        input_as_list = [[char for char in row] for row in mapstr.split("\n")]
    grid = np.array(input_as_list)
    if pad_char is not None:
        grid = np.pad(grid, pad_width=1, mode="constant", constant_values=pad_char)
    return grid


def neighbor_locs(arr, x, y, include_diag=False):
    """Returns the indices of neighbors of a location in a square array."""
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


seen = set()


def get_regions(arr: np.array) -> dict:
    regions = []
    for i in range(1, len(arr) - 1):
        for j in range(1, len(arr) - 1):
            if (i, j) not in seen:
                this_region = find_region(arr, (i, j))
                regions.append(this_region)
    return regions


def find_region(arr, start: tuple[int, int]):
    """Obtain the set of all points within a region, as defined in
    problem text. Based on iterative breadth-first search using queue."""
    label = arr[start]
    queue = [start]
    seen.add(start)
    region_points = set()
    while len(queue) != 0:
        pt = queue.pop(0)
        seen.add(pt)
        region_points.add(pt)
        x_pt, y_pt = pt
        eligible_neighbors = [
            nbr
            for nbr in neighbor_locs(arr, x_pt, y_pt)
            if arr[nbr] == label and nbr not in seen and nbr not in queue
        ]
        for nbr in eligible_neighbors:
            queue.append(nbr)
    region = {"label": label, "points": region_points}
    return region


def get_perimeter(arr, region):
    perimeter = 0
    for pt in region["points"]:
        perimeter += len(
            [
                nbr
                for nbr in neighbor_locs(arr, pt[0], pt[1])
                if arr[nbr] != region["label"]
            ]
        )
    return perimeter


def get_num_sides(region) -> int:
    """
    Find the number of contiguous 'sides' to a region, as defined in Part 2 problem text.
    Do this by sorting point tuples by x and then by y, then converting each
    row 's points into range() notation, where the region's label starts and ends as
    many times as necessary to describe each row of the region.
    After that, each new row finds the number of new sides by summing:

    +2 for every new left bound that wasn't a left bound in previous row,
    +2 for every new right bound that wasn't a right bound in previous row,
    +0 for every range that stays the same from one row to the next
    +X, where X is the difference between number of ranges in the previous row and
     number of ranges in the current row (signed, such that X is positive when
     this row has more ranges than previous, and negative when this row has
     fewer ranges than previous.)

    Example based on "Mobius" paragraph example in problem text:

    AAAAAA  [[1, 7]] -> +2 new left, +2 new right, -1 one new roof.* total: +3 => 3
    AAA  A  [[1, 4], [6, 7]] -> +2 new right, +2 new left, -1 new roof (len(new ranges) - len(old ranges)). total +3 => 6
    AAA  A  [[1, 4], [6, 7]] -> no changes, +0 => 6
    A  AAA  [[1, 2], [4, 7]] -> +2 new left, +2 new right => 10 (-1 new roof, +1 close gap above happen implicitly)
    A  AAA  [[1, 2], [4, 7]] -> no changes, +0  => 10
    AAAAAA  [[1, 7]] -> +1 close out a gap above
    + 1 new floor at bottom => 12

    * could think of this as just len(ranges[0]) - len([]), i.e. 1 - 0
    and the final floor as 0 - len(ranges[-1]), i.e. 0 - (-1)

    it's just len(prev) - len(cur) at every step, is how you do roofs and floors

    """
    pts = region["points"]
    sorted_pts = sorted(pts, key=lambda pt: (pt[0], pt[1]))
    sorted_rows = [list(t[1]) for t in groupby(sorted_pts, lambda pt: pt[0])]
    ranges_in_rows = [ranges_in_row(row) for row in sorted_rows]

    num_sides = 0
    prev_lefts = set()
    prev_rights = set()
    r_prev = []

    for ix, r in enumerate(ranges_in_rows):  # top
        lefts = {i[0] for i in r}
        rights = {i[1] for i in r}
        num_sides += 2 * len(lefts.difference(prev_lefts))
        num_sides += 2 * len(rights.difference(prev_rights))
        num_sides += len(r_prev) - len(r)
        if ix == len(ranges_in_rows) - 1:
            num_sides += len(r)  # close out all remaining regions at bottom
        prev_lefts = lefts
        prev_rights = rights
        r_prev = r
    return num_sides


def ranges_in_row(row: list[tuple[int, int]]):
    """
    Go from a list of tuples of points within a row to the ranges of y-values
    within that row, where range is defined like Python built-in range().
    TODO: see if there's a built-in for this in itertools or something else
    E.g.:
        Input: [(2, 1), (2, 2), (2, 3), (2, 6)] -> Output: [(1, 4), (6, 7)]
        Input: [(5, 1), (5, 4), (5, 5), (5, 6)] -> Output: [(1, 2), (4, 7)]
    """
    yvals = [pt[1] for pt in row]
    ranges = []
    curr_range = []
    for ix, yval in enumerate(yvals):
        if ix == 0:
            curr_range.append(yval)
        if yval > (yvals[ix - 1] + 1):
            curr_range.append(yvals[ix - 1] + 1)
            ranges.append(curr_range)
            curr_range = [yval]
        if ix == len(yvals) - 1:
            curr_range.append(yval + 1)
            ranges.append(curr_range)
            curr_range = [yval]
    return ranges


def run(input, part=1):
    arr = gridify(input, pad_char="0")
    solution = 0
    regs = get_regions(arr)
    for region in regs:
        area = len(region["points"])
        sides_var = get_perimeter(arr, region) if part == 1 else get_num_sides(region)
        price = area * sides_var
        solution += price
    return solution


if __name__ == "__main__":
    input = get_data(day=12, year=2024)
    seen = set()
    part1_solution = run(input)
    print(f"Part 1 solution: {part1_solution}")
    seen = set()
    part2_solution = run(input, part=2)
    print(f"Part 2 solution: {part2_solution}")
