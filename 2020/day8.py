from aocd import get_data
from copy import deepcopy

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=8, year=2020).split("\n")


class Console:
    def __init__(self):
        self.accumulator = 0
        self.address = 0
        self.addresses_seen = []

    def execute_line(self, bootcode):
        instruction = bootcode[self.address]
        op = instruction[:3]
        arg = int(instruction[4:])

        if op == "nop":
            self.address += 1
        elif op == "jmp":
            self.address += arg
        elif op == "acc":
            self.accumulator += arg
            self.address += 1

    def run_bootcode(self, bootcode):
        while True:
            if self.address == len(bootcode):  # termination condition
                print(f"Part 2 solution: {self.accumulator}")
                break
            if self.address in self.addresses_seen:  # oh no, infinite loop!
                return self.accumulator
            self.addresses_seen.append(self.address)
            self.execute_line(bootcode)


def part2():
    # ensure that changes aren't carried over between trials
    fresh_input = deepcopy(input)
    for addr, instruction in enumerate(fresh_input):
        op = instruction[:3]
        arg = instruction[4:]
        c = Console()
        if op == "nop":
            altered_input = deepcopy(fresh_input)
            altered_input[addr] = "jmp " + arg
            c.run_bootcode(altered_input)
        elif op == "jmp":
            altered_input = deepcopy(fresh_input)
            altered_input[addr] = "nop " + arg
            c.run_bootcode(altered_input)


if __name__ == "__main__":
    c = Console()
    print(f"Part 1 solution: {c.run_bootcode(input)}")
    part2()
