from aocd import get_data 
from ast import literal_eval
import re

input = get_data(day=8, year=2015)

def encode(str):
    # Use _ as placeholder to prevent confusion as backslashes are added
    strmod = re.sub(r'"', '_"', str)
    strmod = re.sub(r'\\', '__', strmod)
    # cannot use re.sub() for last one due to "re.error: bad escape (end of pattern) at position 0"
    strmod = strmod.replace('_', '\\')
    return '"' + strmod + '"'

def run(input):
    raw_ct = 0
    processed_ct = 0
    encoded_ct = 0

    for string in input.split('\n'):
        # Raw string is read in from file unmodified, quotes and escapes and all
        raw_len = len(string)
        raw_ct += raw_len

        processed_len = len(literal_eval(string))
        processed_ct += processed_len

        encoded_len = len(encode(string))
        encoded_ct += encoded_len

    return (raw_ct - processed_ct), (encoded_ct - raw_ct)


with open('day8_example.txt') as f:
    example = f.read()

if __name__ == '__main__':
    part1_solution, part2_solution = run(input)
    print(f"Part 1 solution: {part1_solution}")
    print(f"Part 2 solution: {part2_solution}")