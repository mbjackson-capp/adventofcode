from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np

#Problem statement: https://adventofcode.com/2022/day/8

input = get_data(day=8, year=2022).split('\n')
input = np.array([[int(char) for char in str] for str in input], dtype=int)

DIRS = 'NESW'

def full_line(forest, x, y, dir='right'):
    '''Get the coordinates of all points in a given direction from the
    input point, regardless of whether they're visible. Returns the list
    in the order they'd be seen from the tree going outward.'''
    if dir == 'N':
        return [(new_x, y) for new_x in range(0, x)][::-1]
    elif dir == 'E':
        return [(x, new_y) for new_y in range(y+1, len(forest))]
    elif dir == 'S':
        return [(new_x, y) for new_x in range(x+1,len(forest))]
    elif dir == 'W':
        return [(x, new_y) for new_y in range(0, y)][::-1]

def sight_line(forest, x, y, dir, strictly_greater=False):
    '''Get the coordinates of all points visible in a given direction from
    the input point. strictly_greater is True for part 1, False for part 2.'''
    this_height = forest[x][y]
    full = full_line(forest, x, y, dir)
    sightline = []
    for point in full:
        new_x, new_y = point
        if not (strictly_greater and forest[new_x, new_y] >= this_height):
            sightline.append(point)
        if forest[new_x][new_y] >= this_height:
            break
    return sightline

def is_visible(forest, x, y):
    '''Determine whether a tree at the input coordinates is visible from outside
    the forest.'''
    max_x, max_y = forest.shape
    if x == 0 or x == max_x-1 or y == 0 or y == max_y-1:
        return True
    else:
        for dir in DIRS:
            if (len(full_line(forest, x, y, dir)) == 
                len(sight_line(forest, x, y, dir, strictly_greater=True))):
                return True
        return False

def scenic_score(forest, x, y):
    score = 1
    for dir in DIRS:
        score *= len(sight_line(forest, x, y, dir))
    return score

def run(part=1):
    max_x, max_y = input.shape
    ans = 0
    for x in range(max_x):
        for y in range(max_y):
            if part == 1:
                ans += is_visible(input, x, y)
            else:
                ans = max(ans, scenic_score(input, x, y))
    return ans


if __name__ == '__main__':
    f"Part 1 answer: {print(run(part=1))}"
    f"Part 2 answer: {print(run(part=2))}"