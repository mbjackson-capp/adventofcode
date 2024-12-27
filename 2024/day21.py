from aocd import get_data
from functools import cache
from itertools import pairwise  # must be on Python 3.10 or greater
import numpy as np

NUM_KEYPAD = np.array([[7, 8, 9], [4, 5, 6], [1, 2, 3], ["_", 0, "A"]])

DIR_KEYPAD = np.array([["_", "^", "A"], ["<", "v", ">"]])

GAP = "_"


def shortest_paths_from(keypad, start_sym, end_sym) -> list[str]:
    """
    Get all viable shortest paths from one symbol to another on this keyboard.
    Note: Some shortest paths are better than others because they require fewer
    key presses one level 'up'. For example, to go from 0 to 4 on the NUM_KEYPAD,
    you could go '^<^' or '^^<', but the latter is optimal because hitting ^ a
    second time in a row only requires hitting A on the numpad above it, whereas
    the former path requires navigating to <, pressing that, and navigating back to ^.
    As such, paths that alternate up/down direction with left/right direction
    are not retained.
    """
    start = tuple(int(i[0]) for i in np.where(keypad == start_sym))
    x, y = start
    end = tuple(int(i[0]) for i in np.where(keypad == end_sym))
    gap_spot = tuple(int(i[0]) for i in np.where(keypad == GAP))

    x_dist = end[0] - start[0]
    y_dist = end[1] - start[1]

    x_str = ""
    if x_dist < 0:
        x_str += "^" * -x_dist
    elif x_dist > 0:
        x_str += "v" * x_dist

    y_str = ""
    if y_dist < 0:
        y_str += "<" * -y_dist
    elif y_dist > 0:
        y_str += ">" * y_dist

    options = set()
    if (x + x_dist, y) != gap_spot:
        options.add(x_str + y_str)
    if (x, y + y_dist) != gap_spot:
        options.add(y_str + x_str)
    return list(options)


@cache
def expand_button_pushes(input: str, depth: int = 3):
    """
    Recursive function to calculate the number of key presses required on the
    outermost direction keypad in order to type the input code on the innnermost
    (i.e. numeric) keypad. Caches (~= memoizes) results in order to avoid
    repeat computations.

    Example with input '029A' and depth=1:

    -Tack on an 'A' to get: 'A029A'
    -Iterate pairwise over ['A0', '02', '29', '9A']
    -Treat each pair as a start and end:
        A to 0: one optimal path, '<A'
        expand_button_pushes('<A', 0) returns len('<A') = 2
            (now, if depth were > 1 we'd call this again; it'd return len('v<<A>>^A') = 8)

        0 to 2: one optimal path, '^A'
        call expand_button_pushes('^A', 0), return len('^A') = 2

        2 to 9: two possible paths, '^^>A' and '>^^A'
        call expand_button_pushes('^^>', 0) and expand_button_pushes('>^^', 0),
        return the length of the minimum one = 4

        9 to A: one possible path, 'vvvA'
        call expand_button_pushes('vvvA', 0), return length = 4

    sum those all up, cache the value of ('029A', 1) = 12 and values on way up
    """
    if depth == 0:
        return len(input)

    total_len = 0
    # break up input into start-end pairs, then evaluate recursively for every
    # possible path between that start and end
    for pair in pairwise("A" + input):
        first, second = pair
        if first.isnumeric() or second.isnumeric():
            options = shortest_paths_from(NUM_KEYPAD, first, second)
        else:
            options = shortest_paths_from(DIR_KEYPAD, first, second)
            # keeping the min ensures answer is deterministically correct at all depths
        total_len += min(
            [expand_button_pushes(option + "A", depth=depth - 1) for option in options]
        )
    return total_len


def complexity(code: str, depth=3):
    numeric_part = int(code[:-1])
    return numeric_part * expand_button_pushes(code, depth=depth)


def run(input, depth=3):
    total = 0
    for code in input:
        total += complexity(code, depth=depth)
    return total


if __name__ == "__main__":
    input = get_data(day=21, year=2024).split("\n")
    part1_solution = run(input)
    print(f"Part 1 solution: {part1_solution}")
    part2_solution = run(input, depth=26)  # 25 robots AND you
    print(f"Part 2 solution: {part2_solution}")
