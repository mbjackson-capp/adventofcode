from aocd import get_data
import re

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=2, year=2020).split("\n")
input = [re.split(r"-|:?\s", row) for row in input]


def part1():
    valids = 0
    for row in input:
        first_num, second_num, letter, passwd = row
        occurrences = len(re.findall(letter, passwd))
        if (occurrences >= int(first_num)) and (occurrences <= int(second_num)):
            valids += 1
    return valids


def part2():
    valids = 0
    for row in input:
        first_num, second_num, letter, passwd = row
        # use bitwise xor on output of two boolean statements
        if (passwd[int(first_num) - 1] == letter) ^ (
            passwd[int(second_num) - 1] == letter
        ):
            valids += 1
    return valids


if __name__ == "__main__":
    print(part1())
    print(part2())
