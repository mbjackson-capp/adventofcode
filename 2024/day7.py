from aocd import get_data
from operator import add, mul
from copy import deepcopy

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=7, year=2024).split("\n")


def concat(a: int, b: int):
    return int(str(b) + str(a))  # done "backwards" since evaluation is backwards later


def print_op(op):
    """TODO: Make this work properly instead of printing
    [<function concat at 0x1026318a0>, <built-in function mul>] etc."""
    if op == add:
        print("+")
    if op == mul:
        print("*")
    if op == concat:
        print("||")


def run_line(line: str, part=1) -> int:
    result, values = line.split(": ")
    result = int(result)
    values = [int(i) for i in values.split(" ")]
    num_gaps = len(values) - 1
    operator_orders = generate_operator_orders(num_gaps, part=part)
    for order in operator_orders:
        this_order = deepcopy(order)
        these_values = deepcopy(values)
        this_result = do_all_ops(this_order, these_values)
        if this_result == result:  # Success: these operations in this order work
            return result
    return 0


def generate_operator_orders(length: int, part=1):
    if length == 0:
        return [[]]
    else:
        orders_minus_one = generate_operator_orders(length - 1, part=part)
        new_orders = []
        for order in orders_minus_one:
            new_orders.append([add] + order)
            new_orders.append([mul] + order)
            if part == 2:
                new_orders.append([concat] + order)
        return new_orders


def do_all_ops(order, values):
    """Handrolled version of functools.reduce that lets the function change"""
    assert len(order) + 1 == len(values)
    if len(values) == 1:
        return values[0]
    # for some reason (i.e. how function composition works?), this has to be
    # done "backwards" to match desired start-to-end, PEMDAS-ignoring evaluation
    func = order.pop(-1)
    a = values.pop(-1)
    return func(a, do_all_ops(order, values))


def run_all(lines, part=1):
    calibration_result = 0
    for line in lines:
        calibration_result += run_line(line, part=part)
    return calibration_result


if __name__ == "__main__":
    print(f"Part 1 solution: {run_all(input)}")
    print(f"Now running Part 2. This could take a minute...")
    print(f"Part 2 solution: {run_all(input, part=2)}")
