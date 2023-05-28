from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re
from statistics import median

#Problem statement: https://adventofcode.com/2021/day/10

input = get_data(day=10, year=2021).split('\n')

ATOMIC_CHUNKS = r'\(\)|\[\]|\<\>|\{\}'
CLOSE_BRACKETS = r'\)|\]|\>|\}'


def part1():
    return sum([status2(row) for row in input])

def status2(str):
    reduced = reduce(str)
    if len(reduced) == 0: #valid
        return 0
    elif (not has_chunks(reduced)) and has_closing_chars(reduced): #corrupt
        return syntax_error_score(reduced)
    else: #incomplete
        return 0

def reduce(str):
    '''Repeated passes to eliminate all atomic chunks -- e.g. (), [], {} -- 
    until none are left.'''
    if str == re.sub(ATOMIC_CHUNKS, '', str):
        return str
    else:
        return reduce(re.sub(ATOMIC_CHUNKS, '', str))

def has_chunks(str):
    return str != re.sub(ATOMIC_CHUNKS, '', str)

def has_closing_chars(str):
    return re.search(CLOSE_BRACKETS, str) != None

def syntax_error_score(str):
    error_scores = {')': 3, ']': 57, '}': 1197, '>': 25137}
    first_illegal_char = re.findall(CLOSE_BRACKETS, str)[0]
    return error_scores[first_illegal_char]


def part2():
    all_scores = []
    for row in input:
        if status2(row) == 0:
            addend = completion_seq(reduce(row))
            all_scores.append(completion_score(addend))
    return median(all_scores)

def completion_seq(reduced_str):
    '''Gets the corresponding close bracket for each open bracket in a string
    of open brackets, then reverses to put closures in proper nesting order'''
    flipper = {'(':')', '[':']', '{':"}", '<':'>'}
    return ''.join([flipper[char] for char in list(reduced_str)][::-1])

def completion_score(addend):
    char_score = {')': 1, ']': 2, '}': 3, '>': 4}
    total = 0
    for char in addend:
        total = (5 * total) + char_score[char]
    return total


if __name__ == '__main__':
    print(f"Part 1 answer: {part1()}")
    print(f"Part 2 answer: {part2()}")