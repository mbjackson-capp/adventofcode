from aocd import get_data
from computer import Computer

input = [int(i) for i in get_data(day=2, year=2019).split(",")]


def provide_inputs(intcode, noun, verb):
    """
    Replace the values at address 1 and address 2 with inputs.
    """
    intcode[1] = noun
    intcode[2] = verb
    return intcode


c = Computer()


def part1(input, verbose=False):
    restore_1202 = provide_inputs(input, 12, 2)
    part1_output = c.process(restore_1202, verbose=verbose)
    return part1_output


def part2():
    DESIRED_OUTPUT = 19690720
    for noun in range(100):
        for verb in range(100):
            # re-copy from source data every time to hard reset
            inputt = [int(i) for i in get_data(day=2, year=2019).split(",")]
            fresh_intcode = provide_inputs(inputt, noun, verb)
            c = Computer(intcode=fresh_intcode)
            output = c.process(fresh_intcode, verbose=False)
            if output == DESIRED_OUTPUT:
                return (100 * noun) + verb


if __name__ == "__main__":
    print(f"Part 1 solution: {part1(input)}")
    print(f"Part 2 solution: {part2()}")
