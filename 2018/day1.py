from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2018/day/1

#type conversion strips the pluses
input = [int(i) for i in get_data(day=1, year=2018).split('\n')]

def part1():
    return sum(input)

def part2():
    curr_freq = 0
    freqs_seen = {curr_freq}
    while True:
        for change in input:
            curr_freq += change
            if curr_freq in freqs_seen:
                return curr_freq
            freqs_seen.add(curr_freq)

if __name__ == '__main__':
    print(f"Part 1 answer: {part1()}")
    print(f"Part 2 answer: {part2()}")