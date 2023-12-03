from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re
from functools import reduce

#Problem statement: https://adventofcode.com/2023/day/2
 
input = get_data(day=2, year=2023).split('\n')

# Clean input
gamed_out = [re.split(r"Game [\d]{1,3}\: ", i)[1:] for i in input]
# for some reason, without the [0] it produces a list of [[]] instead of a list of []
gamed_out2 = [[re.split('; ', j) for j in game][0] for game in gamed_out]
gamed_out3 = [[re.split(', ', draw) for draw in game] for game in gamed_out2]

def numericize(num_color_str):
    """
    Turn a string like "8 green" into a tuple like (8, "green")
    """
    num, color = re.split(' ', num_color_str)
    num = int(num)
    return (num, color)

gamed_out4 = [[[numericize(result) for result in draw] 
                for draw in game] for game in gamed_out3]

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

def is_game_possible(
    game,
    max_red = MAX_RED,
    max_green = MAX_GREEN,
    max_blue = MAX_BLUE
    ):
    """
    Determine if a game is possible, per criteria for part 1.
    Inputs:
        -game (list of lists of tuples): Each list represents a draw.
        Each item in a draw list is a tuple of form (int, "color"),
        representing the number of cubes of that color in that draw.
    Returns:
        -Boolean (True if game is possible, False otherwise)
    """
    color_maxes = {"red": max_red, "green": max_green, "blue": max_blue}

    for draw in game:
        for this_tuple in draw:
            num, color = this_tuple
            if num > color_maxes[color]:
                return False
    return True

def part1():
    possible_games_id_sum = 0
    for i, game in enumerate(gamed_out4):
        if is_game_possible(game):
            possible_games_id_sum += (i+1) #game IDs are indexed from 1
    return possible_games_id_sum


def min_viable_cubeset(game):
    """
    Determine the smallest number of red, green, and blue cubes possible,
    given a set of draws from the bag (a "game".)

    Inputs:
        -game (list of lists of tuples): Each list represents a draw.
        Each item in a draw list is a tuple of form (int, "color"),
        representing the number of cubes of that color in that draw.
    Returns:
        -min_red, min_green, min_blue (tuple of ints): 
        correct number for each color
    """
    color_maxes = {"red": 0, "green": 0, "blue": 0}

    for draw in game:
        for this_tuple in draw:
            num, color = this_tuple
            if num > color_maxes[color]:
                color_maxes[color] = num

    return color_maxes["red"], color_maxes["green"], color_maxes["blue"]

def part2():
    """Find the 'power' of each set of cubes for each game and add them"""
    power_sum = 0
    for game in gamed_out4:
        power = reduce(lambda a, b: a * b, min_viable_cubeset(game))
        power_sum += power
    return power_sum

if __name__ == "__main__":
    print(f"Part 1 answer: {part1()}")
    print(f"Part 2 answer: {part2()}")