from aocd import get_data
# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
from ast import literal_eval
from functools import cmp_to_key

# Problem statement: https://adventofcode.com/2022/day/13

input = get_data(day=13, year=2022).split('\n')

def in_correct_order(left, right):
    '''Determine if two inputs are in correct order.
    Returns: -1 if the left input is properly "less than" the right input, 0 if
    the inputs cannot be directly ordered, and 1 if the inputs need to be 
    swapped to be put in correct order (for use with with cmp_to_key method)
    '''
    if type(left) == int and type(right) == int:
        if left == right:
            return 0
        elif left < right:
            return -1
        elif right < left:
            return 1
    
    if type(left) == list and type(right) == list:
        #If left side runs out of items first, items are in correct order
        if len(left) == len(right) == 0:
            return 0
        if len(left) == 0 and len(right) != 0:
            return -1
        if len(right) == 0 and len(left) != 0:
            return 1
        else:
            val = in_correct_order(left[0], right[0])
            if val != 0:
                return val
            else:
                return in_correct_order(left[1:], right[1:])

    if type(left) == int and type(right) == list:
        return in_correct_order([left], right)
    if type(left) == list and type(right) == int:
        return in_correct_order(left, [right])
    

def part1_prep():
    input_pairs = []
    for i, packet in enumerate(input):
        if i % 3 == 0:
            left = literal_eval(packet)
        elif i % 3 == 1:
            right = literal_eval(packet)
            input_pairs.append((left, right))
    return input_pairs

def part1():
    total = 0
    input_pairs = part1_prep()
    for i, pair in enumerate(input_pairs):
        idx = i+1
        left, right = pair
        if in_correct_order(left, right) == -1:
            total += idx
    return total


def part2(input): 
    input = [literal_eval(i) for i in [j for j in input if j != '']]
    #add the divider packets
    input.append([[2]])
    input.append([[6]])
    ans = sorted(input, key=cmp_to_key(in_correct_order))

    #+1s to adjust for 1-based indexing in original problem
    decoder_key = (ans.index([[2]]) + 1) * (ans.index([[6]]) + 1)
    return decoder_key


if __name__ == '__main__':
    print(f"Part 1 answer: {part1()}")
    print(f"Part 2 answer: {part2(input)}")