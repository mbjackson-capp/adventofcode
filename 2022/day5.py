from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re
import numpy as np
from copy import deepcopy

#Problem statement: https://adventofcode.com/2022/day/5

input = get_data(day=5, year=2022).split('\n')

STACKS_END = 9
stack_input = input[:STACKS_END]

INSTRUCTIONS_START = 10
instructions = input[INSTRUCTIONS_START:]


def new_stacks():
    '''
    Function to generate the starting input as manipulable stacks of blocks.
    Needs to be called anew each time you operate the crane to reset state
    '''
    #input strings are "horizontal" lines representing all boxes at an elevation.
    #extract boxes and locations at each place on each level
    stacks = []
    STACK_WIDTH = 4
    for line in stack_input:
        newline = []
        for i in range(1, len(line), STACK_WIDTH): #should stop 9 times
            block = line[i]
            newline.append(block)
        stacks.append(newline)

    #rearrange as separate "vertical" stacks with base labels
    stacks = np.array(stacks).T 
    #label is now at right; bottom-to-top goes right-to-left

    stack_dict = {}
    for stack in stacks:
        label = int(stack[-1])
        stack_dict[label] = [block for block in stack[-2::-1] if block != ' ']
        #now, for each stack, bottom-to-top goes left-to-right

    return stack_dict


def operate_crane(stacks, part=1):
    '''
    Inputs:
        -stacks (dict): the starting stacks
        -part (int): determines whether crane uses part 1 rules or part 2 rules
        to move the blocks
    Returns (str): labels on top block of each stack from 1 through 9
    '''
    for item in instructions:
        qty, from_stack, to_stack = [int(i) for i in re.findall(r'[\d]+', item)]
        if part == 1:
            move_p1(stacks, qty, from_stack, to_stack)
        if part == 2:
            move_p2(stacks, qty, from_stack, to_stack)

    blocks_on_top = ""
    for i in range(1, len(stacks)+1):
        blocks_on_top += stacks[i][-1]
    return blocks_on_top
        
def move_p1(stacks, qty, from_stack, to_stack):
    '''
    Move qty blocks, one at a time, from one stack to another. 
    E.g., if:
    -stack 1: from bottom to top ['A', 'B']; stack 2 empty
    then, calling move_p1 (2, 1, 2) results in:
    -stack 1: empty; stack 2: from bottom to top ['B', 'A']
    '''
    for i in range(qty):
        block = stacks[from_stack].pop(-1)
        stacks[to_stack].append(block)

def move_p2(stacks, qty, from_stack, to_stack):
    '''
    Move qty blocks, all at once, from one stack to another.
    E.g., if:
    -stack 1: from bottom to top ['A', 'B']; stack 2 empty
    then, calling move_p2 (2, 1, 2) results in:
    -stack 1: empty; stack 2: from bottom to top ['A', 'B']
    '''
    blocks = []
    for i in range(qty):
        block = stacks[from_stack].pop(-1)
        blocks.insert(0, block)
    stacks[to_stack] += blocks


print(f"Part 1 answer: {operate_crane(new_stacks(), part=1)}")
print(f"Part 2 answer: {operate_crane(new_stacks(), part=2)}")