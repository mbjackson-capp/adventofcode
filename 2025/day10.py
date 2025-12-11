from aocd import get_data
from copy import deepcopy
from typing import List, Tuple
import re
import pulp
from tqdm import tqdm


# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/10

input = get_data(day=10, year=2025)

ON = "#"
OFF = "."


class Machine:
    def __init__(
        self, start_state: List[str], buttons: List[Tuple], joltage_reqs: List[int]
    ):
        self.start_state = start_state
        self.buttons = buttons
        self.joltages = [0] * len(joltage_reqs)
        self.joltage_reqs = joltage_reqs


def parse_machine(row: str) -> Machine:
    """Turn a row of text in machine spec format, e.g.
    '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}'
    into an instance of class Machine."""
    SPLIT_RE = r"(?:(?<=\])\s(?=\()|(?<=\))\s(?=\{))"
    start_str, buttons_str, joltage_str = re.split(SPLIT_RE, row)

    # use [1:-1] string indexing to ignore bracketing symbols
    start_state = [char for char in start_str[1:-1]]

    buttons_text = buttons_str.split(" ")
    buttons = []
    for bt in buttons_text:
        button = tuple(int(i) for i in bt[1:-1].split(","))
        buttons.append(button)

    joltage = [int(i) for i in joltage_str[1:-1].split(",")]

    m = Machine(start_state, buttons, joltage)
    return m


def parse_input(data: str) -> List[Machine]:
    return [parse_machine(row) for row in data.split("\n")]


def toggle(light: str):
    """Simple helper function to turn a particular light on or off."""
    if light == ON:
        return OFF
    elif light == OFF:
        return ON
    else:
        raise ValueError(
            f"use toggle() only on 1-character string equal to {ON} or {OFF}"
        )


def min_presses_to_activate(m: Machine) -> int:
    """Determine the minimum number of buttons that can be pressed on the Machine
    to get its lights into its desired start state.
    Assumes that all provided inputs have a finite answer to this question such
    that infinite loop will always terminate. Do not call on arbitrary input."""
    # after 0 button pushes, just 1 possible world: the world of all lights off
    old_worlds = [deepcopy([OFF for light in m.start_state])]
    n = 1
    while True:
        new_worlds = []
        for ow in old_worlds:
            for button in m.buttons:
                # create a new world state in which just this new button is
                # pushed, after all previous button pushes that have occurred
                # in the old world state
                nw = deepcopy(ow)
                for ix in button:
                    nw[ix] = toggle(nw[ix])
                if nw == m.start_state:
                    return n
                if nw not in new_worlds:
                    new_worlds.append(nw)
        # after n button presses, we have list of all possible states the lights
        # can be in (ignoring redundancies when multiple sequences of button
        # presses would have the same ultimate outcome)
        old_worlds = new_worlds
        n += 1


def button_matrix(m: Machine, transpose=False) -> List[List[int]]:
    """Helper function for Part 2. Re-express the set of buttons as a matrix
    of column vectors, to better work with PuLP linear programming solver."""
    matrix_width = len(m.joltage_reqs)
    matrix = []
    for button in m.buttons:
        col_vector = [0] * matrix_width
        for light in button:
            col_vector[light] = 1
        matrix.append(col_vector)
    if transpose:
        orig_matrix = deepcopy(matrix)
        matrix = [[v[i] for v in orig_matrix] for i in range(matrix_width)]
    return matrix


def min_joltage_button_presses(m: Machine) -> int:
    """Convert a matrix's buttons and joltage requirements into the specifications
    for a linear programming problem, then solve that problem. To wit:

    - Each 'button' can be rewritten a column vector of 1s and 0s, where a 1 at
    index k means that pressing this button toggles light k in the machine
    - The number of times each button is pressed represents a decision variable
    (each of which must be an integer greater than 0)
    - Objective function to minimize is the sum of the decision variables, which
    is the number of button presses total
    - When transposed, a matrix of the button vectors can be multiplied by a vector
    of the decision variables to yield the joltage requirements. Stated differently,
    The k-th row of the transposed "button matrix" represents the buttons that must be
    pressed some number of times to obtain the k-th joltage requirement.

    Consider the first machine in test input data, created from the spec:
    '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}'

    The buttons convert into this matrix:
    [[0 0 0 0 1 1]
    [0 1 0 0 0 1]
    [0 0 1 1 1 0]
    [1 1 0 1 0 0]]
    which, when multiplied by the column vector of decision variables, yields
    [3 5 4 7]

    We want to find the vector [x_0, x_1, x_2, x_3, x_4, x_5] such that:
    - (x_0 + x_1 + x_2 + x_3 + x_4 + x_5) is minimized
    - x_0, x_1, x_2, x_3, x_4, x_5 are all >= 0
    - x_0, x_1, x_2, x_3, x_4, x_5 are all integers
    -  The above matrix multiplication holds, which can be restated as constraints:
        x_4 + x_5 = 3
        x_1 + x_5 = 5
        x_2 + x_3 + x_4 = 4
        x_0 + x_1 + x_3 = 7

    This is well defined mathematically and can be fed into a linear programming solver.

    Indebted to PuLP documentation, and to the following for guidance on flexible
    syntax when number of decision variables and number of constraints aren't
    the same for every input:
    https://or.engineeringcodehub.com/en/latest/CLP/libraries/Python%20PuLP%20Tutorial.html
    """
    num_vars = len(m.buttons)
    variable_names = range(num_vars)
    X = pulp.LpVariable.dicts("x", variable_names, lowBound=0, cat="Integer")
    model = pulp.LpProblem("", pulp.LpMinimize)
    model += pulp.lpSum([1 * X[i] for i in variable_names]), "presses"

    constraints = button_matrix(m, transpose=True)
    joltages = m.joltage_reqs

    for i, constraint in enumerate(constraints):
        model += (
            pulp.lpSum([constraint[j] * X[j] for j in variable_names]) == joltages[i]
        )
    # If desired, replace PULP_CBC_CMD with another solver of your choice
    model.solve(pulp.PULP_CBC_CMD(msg=False))
    min_presses = int(sum([v.value() for v in model.variables()]))
    return min_presses


def solve(data: str, part=1) -> int:
    total_presses = 0
    m_list = parse_input(data)
    for m in tqdm(m_list):
        if part == 1:
            total_presses += min_presses_to_activate(m)
        else:
            total_presses += min_joltage_button_presses(m)
    return total_presses


if __name__ == "__main__":
    p1_ans = solve(input, part=1)
    print(f"Part 1 answer: {p1_ans}")
    p2_ans = solve(input, part=2)
    print(f"Part 2 answer: {p2_ans}")
