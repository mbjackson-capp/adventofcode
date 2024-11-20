from aocd import get_data
from computer import Computer

# Your inputs may vary
PART_1_INPUT = 1
PART_2_INPUT = 5

input = [int(i) for i in get_data(day=5, year=2019).split(",")]
c = Computer()
print(
    f"Part 1 solution: {c.process(input, preset_inputs=[PART_1_INPUT], verbose=False)}"
)

# "reset"
input = [int(i) for i in get_data(day=5, year=2019).split(",")]
c = Computer()
print(
    f"Part 2 solution: {c.process(input, preset_inputs=[PART_2_INPUT], verbose=False)}"
)
