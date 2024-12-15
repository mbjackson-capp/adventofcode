from aocd import get_data
import numpy as np
import re
from numpy.linalg import solve

BIG_NUMBER = 10000000000000


def find_button_presses(machine, part=1):
    machine = machine.split("\n")
    buttons = []
    for button in range(2):
        buttons.append(re.findall(r"(?:X|Y)\+([0-9]+)", machine[button]))
    solutions = re.findall(r"(?:X|Y)=([0-9]+)", machine[-1])
    buttons = np.array(buttons, dtype=int).T
    solutions = np.array(solutions, dtype=float)
    if part == 2:
        solutions += BIG_NUMBER
    answer = solve(buttons, solutions)
    a_sol, b_sol = answer
    # numpy is not exact, e.g. [21. 7.] might be [21.000000000001, 6.999999999999]
    # or similar under the hood, so absolute equality check has many false negatives
    ans_rounded = np.array([round(a_sol), round(b_sol)], dtype=int)
    # closeness checks may fail in part 2 for original numbers, but succeed
    # when using only post-decimal part of solution (probably bc part 2 numbers are very large)
    diffs_from_zero = [answer[i] - ans_rounded[i] for i in range(2)]
    # atol, rtol set so only second and fourth machine in part 2 example return a valid cost
    if np.all(np.isclose(diffs_from_zero, [0, 0], atol=1e-4, rtol=1e-4)):
        return ans_rounded
    return None


def run(machines, part=1):
    total_cost = 0
    machines = machines.split("\n\n")
    for machine in machines:
        presses = find_button_presses(machine, part=part)
        if presses is not None:
            a_presses, b_presses = presses
            this_cost = (3 * a_presses) + b_presses
            total_cost += this_cost
    return total_cost


input = get_data(day=13, year=2024)
part1_solution = run(input)
print(f"Part 1 solution: {part1_solution}")

part2_solution = run(input, part=2)
print(f"Part 2 solution: {part2_solution}")
