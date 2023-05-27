from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
from statistics import mean, median
from math import floor, ceil

#Problem statement: https://adventofcode.com/2021/day/7

input = [int(i) for i in get_data(day=7, year=2021).split(',')]

def part1(input):
    """Thanks to ShapiroA from LearnedLeague ("Pencil and Paper Math 8") for the 
    insight that 'the ideal meeting point must be the median [crab]'s location'"""
    median_crab = int(median(input))
    return sum([abs(crab - median_crab) for crab in input])

def part2(input):
    """This is just OLS regression in 1 dimension, for which the predicted value is
    the mean. Since mean is decimal and crabs only travel to integer values, we have
    to check the integers below and above the mean to see which is lower cost"""
    return min(part2_fuel_sum(floor(mean(input))),
               part2_fuel_sum(ceil(mean(input))))

def part2_fuel_sum(place):
    """Closed form of part 2 fuel burn rate: nth triangular number, where n is 
    distance crab has to travel"""
    sum = 0
    for crab in input:
        dist = abs(crab - place)
        sum += (dist * (dist + 1)) / 2
    return int(sum)

if __name__ == '__main__':
    print(f"Part 1 solution: {part1(input)}")
    print(f"Part 2 solution: {part2(input)}")
