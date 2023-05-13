from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2020/day/1

input = [int(i) for i in get_data(day=1, year=2020).split('\n')]

def part1():
    for i, num in enumerate(input):
        for j in range(i+1, len(input)):
            if num + input[j] == 2020:
                return num * input[j]

def part2():
    for i, num in enumerate(input):
        for j in range(i+1, len(input)): 
            for k in range(j+1, len(input)):
                if num + input[j] + input[k] == 2020:
                    return num * input[j] * input[k]

if __name__ == '__main__':
    print(part1())
    print(part2())