from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re

#Problem statement: https://adventofcode.com/2022/day/2

#'A' represents 'rock', 'B' represents 'paper', 'C' represents 'scissors'
RPS = {'A': {'beats': 'C', 'loses_to': 'B', 'score': 1},
       'B': {'beats': 'A', 'loses_to': 'C', 'score': 2},
       'C': {'beats': 'B', 'loses_to': 'A', 'score': 3}}

input = get_data(day=2, year=2022)

def part1(input) -> int:
    #https://unix.stackexchange.com/questions/506534/multiple-replacements-using-regular-expressions-in-python
    part1_notation = (('X', 'A'), ('Y', 'B'), ('Z', 'C'))
    for old, new in part1_notation:
        input = re.sub(old, new, input)
    input = re.split('\n', input)
    
    total_score = 0
    for game in input:
        opponent, you = game.split(' ')
        total_score += play(opponent, you)
    return total_score

def part2(input) -> int:
    input = re.split('\n', input)
    total_score = 0
    for game in input:
        opponent, you = game.split(' ')
        if you == 'X': #lose
            you = RPS[opponent]['beats']
        elif you == 'Y': #draw
            you = opponent
        elif you == 'Z': #win
            you = RPS[opponent]['loses_to']
        total_score += play(opponent, you)
    return total_score

def play(opponent, you):
    '''
    Helper function that plays a game of rock-paper-scissors, where 'A' is rock,
    'B' is paper, and 'C' is scissors.
    Inputs: 
        -opponent, you (1-character string): should be in ['A', 'B', 'C']
    Returns: outcome score of game where each player played those moves
    '''
    game_score = 0
    if you == opponent:
        game_score += 3
    elif you == RPS[opponent]['loses_to']:
        game_score += 6
    elif you == RPS[opponent]['beats']:
        pass
    game_score += RPS[you]['score']
    return game_score


if __name__ == '__main__':
    print(part1(input))
    print(part2(input))