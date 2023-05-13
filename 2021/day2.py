from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re

#Problem statement: https://adventofcode.com/2021/day/2

class Sub():
    def __init__(self, h=0, d=0, aim=0):
        self.h = 0
        self.d = 0
        self.aim = 0

    def answer(self):
        return self.h * self.d

input = get_data(day=2, year=2021).split('\n')

print(input)

def part1():
    sub = Sub()
    for command in input:
        dir, num = command.split(' '); num = int(num)
        if dir == 'forward':
            sub.h += num
        elif dir == 'down':
            sub.d += num
        elif dir == 'up':
            sub.d -= num
    
    return sub.answer()

def part2():
    sub = Sub()
    for command in input:
        dir, num = command.split(' '); num = int(num)
        if dir == 'forward':
            sub.h += num
            sub.d += sub.aim * num
        elif dir == 'down':
            sub.aim += num
        elif dir == 'up':
            sub.aim -= num
    
    return sub.answer()

if __name__ == '__main__':
    print(f"The answer to part 1 is: {part1()}")
    print(f"The answer to part 2 is: {part2()}")