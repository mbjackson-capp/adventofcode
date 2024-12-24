from aocd import get_data

input = get_data(day=24, year=2024)


def parse_input(input):
    circuit = {}
    starting, logic = input.split("\n\n")
    for line in starting.split("\n"):
        gate, val = line.split(": ")
        circuit[gate] = int(val)

    logic = logic.split("\n")
    # Rules are not in order, so you can't just evaluate this in order
    while len(logic) > 0:
        succeeded = [False for _ in logic]
        for ix, line in enumerate(logic):
            formula, gate = line.split(" -> ")
            input1, func, input2 = formula.split(" ")
            try:
                if func == "AND":
                    circuit[gate] = circuit[input1] & circuit[input2]
                elif func == "XOR":
                    circuit[gate] = circuit[input1] ^ circuit[input2]
                elif func == "OR":
                    circuit[gate] = circuit[input1] | circuit[input2]
                succeeded[ix] = True
            except KeyError:
                continue
        logic = [line for ix, line in enumerate(logic) if not succeeded[ix]]

    return circuit


def produce_number(circuit: dict) -> int:
    after_z = 0
    binary_rep = ""
    while f"z{str(after_z).rjust(2, '0')}" in circuit:
        new_digit = circuit[f"z{str(after_z).rjust(2, '0')}"]
        binary_rep = str(new_digit) + binary_rep
        after_z += 1
    return int(binary_rep, 2)


def part1():
    circuit = parse_input(input)
    result = produce_number(circuit)
    return result


if __name__ == "__main__":
    part1_solution = part1()
    print(f"Part 1 solution: {part1_solution}")

    # TODO: Part 2
