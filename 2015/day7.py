from aocd import get_data

data = get_data(day=7, year=2015).split("\n")
SIXTEEN_BIT_MAX = 65536
memo_table = {}


def NOT(val: int):
    return ~val % SIXTEEN_BIT_MAX


def OR(val1: int, val2: int):
    return (val1 | val2) % SIXTEEN_BIT_MAX


def AND(val1: int, val2: int):
    return (val1 & val2) % SIXTEEN_BIT_MAX


def LSHIFT(val: int, shift_by: int):
    return (val << shift_by) % SIXTEEN_BIT_MAX


def RSHIFT(val: int, shift_by: int):
    return (val >> shift_by) % SIXTEEN_BIT_MAX


def func_from_str(funcname):
    funcs = {"NOT": NOT, "OR": OR, "AND": AND, "LSHIFT": LSHIFT, "RSHIFT": RSHIFT}
    return funcs[funcname]


def sanitize_left(left):
    args = left.split(" ")
    if len(args) == 1 and not args[0].isnumeric():
        return args[0]
    elif len(args) == 1:
        return int(args[0])
    elif len(args) == 2 and args[0] == "NOT":
        return (NOT, args[1])
    elif len(args) == 3:
        operand1, my_func, operand2 = args
        return (func_from_str(my_func), operand1, operand2)


def make_left_of_dict(circuit: list[str]):
    left_of_dict = {}
    for rule in circuit:
        left, right = rule.split(" -> ")
        left_of_dict[right] = sanitize_left(left)
    return left_of_dict


def find_final_wire_value(rules: dict, data):
    """Must do memoization to prevent extremely long runtimes with excessive
    repeated calculations"""
    # Base case: evaluating an integer. you're done
    if type(data) == int:
        return data
    expanded = rules[data]
    # "Base"-ish case: answer has been memoized. go get it
    if expanded in memo_table:
        return memo_table[expanded]
    # Base case: you found an integer. you're done
    if type(expanded) == int:
        return expanded
    # Recursive cases
    elif type(expanded) == str and not expanded.isnumeric():
        return find_final_wire_value(rules, expanded)
    else:
        operation = expanded[0]
        arg1 = (
            int(expanded[1])
            if (type(expanded[1]) == str and expanded[1].isnumeric())
            else expanded[1]
        )
        if operation == NOT:
            solution = NOT(find_final_wire_value(rules, arg1))
        else:
            arg2 = (
                int(expanded[2])
                if (type(expanded[2]) == str and expanded[2].isnumeric())
                else expanded[2]
            )
            solution = operation(
                find_final_wire_value(rules, arg1),
                find_final_wire_value(rules, arg2),
            )
        if type(solution) == int:
            memo_table[expanded] = solution
        return solution


if __name__ == "__main__":
    rules = make_left_of_dict(data)

    overwrite_value = find_final_wire_value(rules, "a")
    print(f"Part 1 solution: {overwrite_value}")

    rules["b"] = overwrite_value
    memo_table = {}
    part2_solution = find_final_wire_value(rules, "a")
    print(f"Part 2 solution: {part2_solution}")
