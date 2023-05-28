from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np

#Problem statement: https://adventofcode.com/2021/day/11

def step0_octopi():
    '''Since step modifies an ndarray in-place, call part1 and part2 with this
    as its argument to start from step 0 / input state'''
    input = get_data(day=11, year=2021).split('\n')
    input = np.array([[int(char) for char in str] for str in input], dtype=int)
    return input


def neighbor_locs(sqarray, x, y, include_diag=True):
    '''Returns the indices of neighbors of a location in a square array.
    Reused with modifications from my 2021 Day 9.'''
    neighbor_locs = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            if not include_diag and dx != 0 and dy != 0:
                continue
            else:
                this_x = x + dx
                this_y = y + dy
                if (this_x >= 0 and this_y >= 0
                    and this_x < len(sqarray) and this_y < len(sqarray)):
                    neighbor_locs.append((this_x, this_y))
    return neighbor_locs

def step(octopi):
    flashes_this_step = 0
    octopi += 1
    while octopi[octopi > 9].size > 0:
        flash_status_now = (octopi > 9).copy()
        octopi[octopi > 9] = -1 #represents 'flash'
        for index, flashed in np.ndenumerate(flash_status_now):
            if flashed:
                x, y = index
                neighbors = neighbor_locs(octopi, x, y)
                for loc in neighbors:
                    this_x, this_y = loc
                    if octopi[this_x][this_y] >= 0:
                        octopi[this_x][this_y] += 1
    flashes_this_step += len(octopi[octopi == -1])
    octopi[octopi == -1] = 0
    return flashes_this_step

def part1(input):
    total_flashes = 0
    for i in range(100):
        total_flashes += step(input)
    return total_flashes

def part2(input):
    step_count = 0
    while True:
        step_count += 1
        if step(input) == 100:
            return step_count

if __name__ == '__main__':
    print(f"Part 1 answer: {part1(step0_octopi())}")
    print(f"Part 2 answer: {part2(step0_octopi())}")