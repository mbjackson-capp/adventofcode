from aocd import get_data
import numpy as np

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2016/day/2

input = get_data(day=2, year=2016).split("\n")


keypad1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
keypad2 = np.array(
    [
        [None, None, 1, None, None],
        [None, 2, 3, 4, None],
        [5, 6, 7, 8, 9],
        [None, "A", "B", "C", None],
        [None, None, "D", None, None],
    ]
)


def move(finger: tuple[int, int], keypad: np.array, step: str) -> tuple[int, int]:
    x, y = finger
    max_x = len(keypad)
    max_y = len(keypad[0])
    assert step in ["U", "R", "D", "L"], "Invalid step instruction received!"
    if step == "U" and x > 0 and keypad[x - 1][y] is not None:
        x -= 1
    elif step == "R" and y < max_y - 1 and keypad[x][y + 1] is not None:
        y += 1
    elif step == "D" and x < max_x - 1 and keypad[x + 1][y] is not None:
        x += 1
    elif step == "L" and y > 0 and keypad[x][y - 1] is not None:
        y -= 1
    new_finger = (x, y)
    return new_finger


def press(finger: tuple[int, int], keypad: np.array) -> int:
    x, y = finger
    return str(keypad[x][y])


def do_instructions(keypad: np.array, lines: list[str]) -> int:
    code = ""
    finger = (1, 1)
    for line in lines:
        for _, step in enumerate(line):
            finger = move(finger, keypad, step)
        new_digit = press(finger, keypad)
        code += new_digit
    return code


if __name__ == "__main__":
    print(f"Part 1 solution: {do_instructions(keypad1, input)}")
    print(f"Part 2 solution: {do_instructions(keypad2, input)}")
