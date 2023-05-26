from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import math
import re

#Problem statement: https://adventofcode.com/2021/day/3

input = get_data(day=4, year=2021).split('\n')

bingo_calls = [int(i) for i in input[0].split(',')]

BOARDS_START_ROW = 2
all_boards = []
curr_board = []
for row in input[BOARDS_START_ROW:]:
    if row:
        curr_board.append(np.array([i for i in re.split(r'\s+', row) if i], 
                                    dtype=int))
    else:
        curr_board = np.array(curr_board)
        all_boards.append(curr_board)
        curr_board = []
#handle last board, since there's no blank line at end of file
curr_board = np.array(curr_board)
all_boards.append(curr_board)

#numpy array of 100 boards, each 5x5
all_boards = np.array(all_boards)

winners = []
first_winner_found = False

while len(bingo_calls) != 0:
    curr_call = bingo_calls.pop(0)
    #use -1 to represent already-called spots
    all_boards[all_boards == curr_call] = -1

    for j, board in enumerate(all_boards):
        empty_row_check = np.sum(board < 0, axis=0)
        empty_col_check = np.sum(board < 0, axis=1)
        if ((np.max(empty_row_check == 5) or np.max(empty_col_check == 5)) 
            and j not in winners):
            if not first_winner_found:
                first_winner_found = True
                print(f"Part 1 solution: {np.sum(board[board >= 0]) * curr_call}")
            winners.append(j)
            if len(winners) == len(all_boards):
                print(f"Part 2 solution: {np.sum(board[board >= 0]) * curr_call}")
                break