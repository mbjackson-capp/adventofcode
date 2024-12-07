from aocd import get_data
import re

input = get_data(day=6, year=2015).split("\n")


def new_grid():
    return {(i, j): 0 for i in range(1000) for j in range(1000)}


def parse_instruction(instr: str):
    action, start, _, finish = re.split(r"(?<!turn)\s", instr)
    start = [int(i) for i in start.split(",")]
    finish = [int(i) for i in finish.split(",")]
    return action, start, finish


def run_instructions(instrs: list[str], part=1, verbose=False):
    grid = new_grid()
    for instr in instrs:
        if verbose:
            print(instr)
        action, start, finish = parse_instruction(instr)
        x_start, y_start = start
        x_end, y_end = finish
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                if part == 1:
                    part1_core(action, x, y, grid)
                else:
                    part2_core(action, x, y, grid)
    return sum(grid.values())


def part1_core(action, x, y, grid):
    if action == "turn on":
        grid[(x, y)] = 1
    elif action == "turn off":
        grid[(x, y)] = 0
    elif action == "toggle":
        grid[(x, y)] = 1 if grid[(x, y)] == 0 else 0


def part2_core(action, x, y, grid):
    if action == "turn on":
        grid[(x, y)] += 1
    elif action == "turn off":
        grid[(x, y)] = max(grid[(x, y)] - 1, 0)
    elif action == "toggle":
        grid[(x, y)] += 2


print(f"Running Part 1. This could take a few seconds...")
print(f"Part 1 solution: {run_instructions(input, part=1)}")

print(f"Running Part 2. This could take a few seconds...")
print(f"Part 2 solution: {run_instructions(input, part=2)}")
