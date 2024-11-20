from aocd import get_data
from computer import Computer

input = [int(i) for i in get_data(day=5, year=2019).split(",")]

c = Computer()

# Input the ID from your instructions upon running.
c.process(input, verbose=False)
