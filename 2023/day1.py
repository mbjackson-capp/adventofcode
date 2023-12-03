from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re

#Problem statement: https://adventofcode.com/2023/day/1
 
input = get_data(day=1, year=2023).split('\n')
only_digits_input = [re.sub(r'[A-Za-z]+', '', i) for i in input]

def calibration_digits(digit_str):
    '''
    Get the first and last digit of a string whose characters are digits.
    Note: If input string has only one digit, it'll return that digit
    concatenated to itself.
    '''
    first = digit_str[0]
    last = digit_str[-1]

    return first + last

part1_calibrations = [int(calibration_digits(i)) for i in only_digits_input]
part1 = sum(part1_calibrations)

# keep values as strings to prevent leading-zero truncation
name_to_digit = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

def numberize(digit_str):
    '''Convert number words into numbers, leaving all else constant'''
    if digit_str in name_to_digit:
        return name_to_digit[digit_str]
    elif digit_str.isnumeric():
        return digit_str

# Issue: something like "zfxbzhczcx9eightwockk" has a string blending two
# number names, "eightwo", in it. Both numbers are needed to get accurate
# first and last digit for full line

any_blend = r"(zerone|oneight|twone|threeight|fiveight|sevenine|eightwo)"

# Source for passing functions to re.sub replacement pattern:
# https://stackoverflow.com/questions/12597370/python-replace-string-pattern-with-output-of-function

def unblend(match):
    str = match.group()
    unblend_dict = {
        "zerone" : "zeroone",
        "oneight" : "oneeight",
        "twone" : "twoone",
        "threeight" : "threeeight",
        "fiveight": "fiveeight",
        "sevenine": "sevennine",
        "eightwo": "eighttwo"
    }
    if str in unblend_dict:
        return unblend_dict[str]
    else:
        return str

unblended_input = [re.sub(any_blend, unblend, i) for i in input]

any_num = r"(zero|one|two|three|four|five|six|seven|eight|nine|\d)"

new_digits = [re.findall(any_num, i) for i in unblended_input]
newer_digits = [''.join([numberize(j) for j in line]) for line in new_digits]

part2_calibrations = [int(calibration_digits(i)) for i in newer_digits]
part2 = sum(part2_calibrations)


if __name__ == '__main__':
    print(f"Part 1 answer: {part1}")
    print(f"Part 2 answer: {part2}")