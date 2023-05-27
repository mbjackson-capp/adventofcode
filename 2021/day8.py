from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2021/day/8

input = [i.split(' | ') for i in get_data(day=8, year=2021).split('\n')]

PART_1_NUMS = [1, 4, 7, 8]

def run(input, part1=True):
    signal_patterns = [i[0].split(' ') for i in input]
    output_values = [i[1].split(' ') for i in input]
    total = 0
    for j, signal in enumerate(signal_patterns):
        decoding = decode(signal)
        digit_sets = [set(digit) for digit in output_values[j]]
        output_digits = [get_key(digit, decoding) for digit in digit_sets]
        if part1:
            total += len([i for i in output_digits if i in PART_1_NUMS])
        else:
            output_num = int(''.join([str(i) for i in output_digits]))
            total += output_num
    return total

def get_key(val, dict):
    for k, v in dict.items():
        if val == v:
            return k

def decode(signal_pattern):
    '''
    Deduce which subset of letters a-g corresponds to each digit from 0 to 9.
    Input: 
        -signal_pattern (str): pattern on left side of '|' on a line of input
        (e.g. 'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb')
    Returns (dict): dict where each key is a digit, and each value is the set 
    of characters corresponding to that digit
    '''
    code = {'top': None, 'ul': None, 'ur': None, 'mid': None, 
            'll': None, 'lr': None, 'bot': None}
    digit_signals = {}
    ALL_RELAYS = {char for char in 'abcdefg'}
    signal_pattern.sort(key=len)

    #we know the component signals of digits with unique numbers of segments
    digit_signals[1] = {char for char in signal_pattern[0]}
    digit_signals[7] = {char for char in signal_pattern[1]}
    digit_signals[4] = {char for char in signal_pattern[2]}
    digit_signals[8] = ALL_RELAYS
    #the unique segment in 7 is top
    code['top'] = (digit_signals[7] - digit_signals[1]).pop()

    #find six-character signal with every segment of 4 or 7 in it. that's 9
    found_so_far = digit_signals[4] | digit_signals[7]
    nine = [signal for signal in signal_pattern 
            if (len(signal) == 6 and set(signal).intersection(found_so_far) == found_so_far)]
    digit_signals[9] = set(nine[0])
    #the new segment in 9 is bottom
    code['bot'] = digit_signals[9].difference(found_so_far).pop()
    #the only segment not in 9 is lower left
    code['ll'] = ALL_RELAYS.difference(digit_signals[9]).pop()

    #find six-character signal containing both segments of 1. that's 0
    zero = [signal for signal in signal_pattern
            if len(signal) == 6 and 
            set(signal) not in digit_signals.values() and
            set(signal) | digit_signals[1] == set(signal)]
    digit_signals[0] = set(zero[0])
    #the only segment not in 0 is middle
    code['mid'] = ALL_RELAYS.difference(digit_signals[0]).pop()

    #find remaining six-character signal. that's 6
    six = [signal for signal in signal_pattern
            if len(signal) == 6 and
            set(signal) not in digit_signals.values()]
    digit_signals[6] = set(six[0])

    #now we can deduce all remaining character-to-segment correspondences
    code['ur'] = ALL_RELAYS.difference(digit_signals[6]).pop()
    code['lr'] = digit_signals[1].difference(set(code['ur'])).pop()
    code['ul'] = ALL_RELAYS.difference(set(code.values())).pop()

    #and signal sets for remaining unsolved digits
    digit_signals[2] = {code[i] for i in ['top', 'ur', 'mid', 'll', 'bot']}
    digit_signals[3] = {code[i] for i in ['top', 'ur', 'mid', 'lr', 'bot']}
    digit_signals[5] = {code[i] for i in ['top', 'ul', 'mid', 'lr', 'bot']}

    return digit_signals


print(f"Part 1 answer: {run(input)}")
print(f"Part 2 answer: {run(input, part1=False)}")