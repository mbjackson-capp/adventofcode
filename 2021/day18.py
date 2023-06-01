from aocd import get_data
# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re
from math import floor, ceil
from ast import literal_eval

#Problem statement: https://adventofcode.com/2021/day/18

input = get_data(day=18, year=2021).split('\n')
    
def add(left, right):
    '''Add two snailfish numbers by making them the left and right elements of
    a pair and then reducing the resultant.'''
    return reduce([left, right])

def reduce(snail):
    while not is_reduced(snail):
        if max_depth(snail) >= 4:
            snail = explode(snail)
            continue
        if has_multidigit(snail):
            snail = split_leftmost(snail)
            continue
    return snail

def is_reduced(snail):
    return (max_depth(snail) < 4 and not has_multidigit(snail))

def max_depth(snail):
    '''Calculate how many nested pairs deep the most nested pair is within a
    snailfish number'''
    if type(snail) == int:
        return 0
    elif type(snail) == list:
        left, right = snail
        if type(left) == int and type(right) == int:
            return 0
        else:
            return 1 + max(max_depth(left), max_depth(right))

def has_multidigit(snail):
    if type(snail) == int:
        return snail > 9
    elif type(snail) == list:
        left, right = snail
        return has_multidigit(left) or has_multidigit(right)
    
def explode(snail):
    '''Explode the leftmost simple pair nested inside 4 pairs'''
    if not type(snail) == str:
        snail = str(snail)
    lhs, exploding, rhs = leftmost_4deep(snail)
    exploded_L, exploded_R = literal_eval(exploding)
    # (last_num_left>9) == 0 or 1 is used to rejoin exploded string 
    # properly even if number being overwritten is two digits long
    if re.findall('\d', lhs):
        last_num, l_idx = [(int(m.group()), m.start()) for m in re.finditer('\d{1,2}', lhs)][-1]
        new_last = last_num + exploded_L
        lhs = lhs[:l_idx] + str(new_last) + lhs[l_idx+1+(last_num>9):]
    if re.findall('\d', rhs):
        first_num, r_idx = [(int(m.group()), m.start()) for m in re.finditer('\d{1,2}', rhs)][0]
        new_first = first_num + exploded_R
        rhs = rhs[:r_idx] + str(new_first) + rhs[r_idx+1+(first_num>9):]
    exploded_snail = lhs + '0' + rhs
    return literal_eval(exploded_snail)

def leftmost_4deep(snail):
    '''Progress through string representation of the snailfish number, tracking
    nesting level until the exploding pair is found. Returns that pair, along 
    with the whole substrings to the left and to the right of it'''
    if type(snail) != str:
        snail = str(snail)
    depth = -1
    lhs = exploding = rhs = ''

    for idx, char in enumerate(snail):
        if char == '[':
            depth += 1
        if char == ']':
            if depth == 4:
                exploding += char
                rhs = snail[idx+1:]
                break
            depth -= 1
        if depth == 4:
            exploding += char
        else:
            lhs += char

    return lhs, exploding, rhs

def split_leftmost(snail):
    '''Split the leftmost simple pair with a two-digit number in it'''
    snail_str = str(snail)
    double_digit = re.findall(r'\d{2}', snail_str)[0]
    snail_str = re.sub(double_digit, 'REPLACE', snail_str, count=1)

    left = floor(int(double_digit) / 2)
    right = ceil(int(double_digit) / 2)
    new_pair = f'[{left},{right}]'
    snail_str = re.sub('REPLACE', new_pair, snail_str)
    return literal_eval(snail_str)        

def magnitude(snail):
    if type(snail) == int:
        return snail
    elif type(snail) == list:
        left, right = snail
        return 3 * magnitude(left) + 2 * magnitude(right)


def part1(snail_list):
    total = literal_eval(snail_list[0])
    for snail in snail_list[1:]:
        snail = literal_eval(snail)
        total = add(total, snail)
    return magnitude(total)

def part2(snail_list):
    snails = [literal_eval(snail) for snail in snail_list]
    max_sum_magnitude = 0
    for i in range(len(snails)):
        for j in range(i+1, len(snails)):
            sum1 = magnitude(add(snails[i], snails[j]))
            sum2 = magnitude(add(snails[j], snails[i]))
            max_sum_magnitude = max(sum1, sum2, max_sum_magnitude)
    return max_sum_magnitude


if __name__ == '__main__':
    print(f"Part 1 answer: {part1(input)}") #runtime: ~1sec
    print(f"Part 2 answer: {part2(input)}") #runtime: ~12sec

