from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re
from functools import reduce

#Problem statement: https://adventofcode.com/2023/day/6a
input = get_data(day=6, year=2023).split('\n')

def split_and_intify(str):
    '''
    Split a string of numbers at the spaces and keep only the integers.
    Reused from my solution for 2023, day 4.
    '''
    splitted = re.split(r'\s+', str)
    splitted = [int(i) for i in splitted if i.isnumeric()]
    return splitted

times, distances = [split_and_intify(i) for i in input]
races = list(zip(times, distances)) #you can just keep it as a zip object

def can_win(hold_time: int, race) -> bool:
    '''
    Return True if it's possible to beat the record by holding the
    button for hold_time milliseconds, False otherwise.
    '''
    rec_time, rec_dist = race
    your_dist = hold_time * (rec_time - hold_time)
    return your_dist > rec_dist

example_race = (7, 9)

def ways_to_win(race) -> int:
    '''
    Calculate how many ways it is possible to win a given race.
    Input: race (tuple (int, int)): record time, record distance
    '''
    ways = 0
    rec_time, rec_dist = race
    for hold_t in range(0, rec_time + 1):
        if can_win(hold_t, race):
            ways += 1
        elif ways > 0:
            break
    return ways

part1 = reduce(lambda a,b: a*b, [ways_to_win(race) for race in races])
print(f"Part 1 answer: {part1}")

part2_time = int(''.join([str(t) for t in times]))
part2_dist = int(''.join([str(d) for d in distances]))
part2_race = (part2_time, part2_dist)

# Takes ~5-6 seconds to run. Consider replacing one or both helper functions
# with closed form formula to speed up evaluation
print(f"Part 2 answer: {ways_to_win(part2_race)}")