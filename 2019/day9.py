from aocd import get_data
from computer import Computer

input = [int(i) for i in get_data(day=9, year=2019).split(",")]

c = Computer()

part1 = c.process(intcode=input, initial_inputs=[1])
print(f"Part 1 solution: {part1}")
part2 = c.process(intcode=input, reset=True, initial_inputs=[2])
print(f"Part 2 solution: {part2}")
