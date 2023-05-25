from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import operator

#Problem statement: https://adventofcode.com/2021/day/3

input = get_data(day=3, year=2021).split('\n')
input = np.asarray([list(i) for i in input], dtype=int)

def part1(input):
    count = np.count_nonzero(input, axis=0)

    MAJORITY_THRESHOLD = len(input) / 2
    gamma_rate = ''.join([str(int(i > MAJORITY_THRESHOLD)) for i in count])
    epsilon_rate = ''.join([str(int(i < MAJORITY_THRESHOLD)) for i in count])

    power_consumption = int(gamma_rate, 2) * int(epsilon_rate, 2)
    return power_consumption


def part2(input):
    return (int(part2_rating(input, 'oxygen'), 2) * 
            int(part2_rating(input, 'co2'), 2))

def part2_rating(input, substance):
    '''Whittle down input until you get a unique binary string for substance'''
    ops = {'oxygen': operator.ge, 'co2': operator.lt}

    for pos in range(input.shape[1]):
        majority_threshold = len(input) / 2
        number_of_ones = np.count_nonzero(input[:,pos])
        if len(input) == 1: 
            return ''.join([str(i) for i in input.flatten()])

        operation = ops.get(substance)
        if operation(number_of_ones, majority_threshold):
            input = np.array([i for i in input if i[pos] == 1])
        else:
            input = np.array([i for i in input if i[pos] == 0])

    return ''.join([str(i) for i in input.flatten()])


if __name__ == '__main__':
    print(f"Part 1 solution: {part1(input)}")
    print(f"Part 2 solution: {part2(input)}")
