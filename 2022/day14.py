from aocd import get_data
# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import time

input = get_data(day=14, year=2022).split('\n')

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                getattr(other, 'x', None) == self.x and
                getattr(other, 'y', None) == self.y)

    def __hash__(self):
        return hash(self.x + self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"


def fall(grain, blocked, floor=None):
    '''Inputs:
        -grain (Point object)
        -blocked (set of Points)
        -floor (int)'''
    if floor and grain.y == floor - 1: #sand settles ABOVE floor, not ON it
        return True
    if Point(grain.x, grain.y+1) in blocked:
        if Point(grain.x-1, grain.y+1) in blocked:
            if Point(grain.x+1, grain.y+1) in blocked:
                return True
            else:
                grain.x += 1
                grain.y += 1
        else:
            grain.x -= 1
            grain.y += 1
    else:
        grain.y += 1
    return False



def draw(endpt1, endpt2):
    '''Adds all points between two endpoints, inclusive, to a set of blocked points.
    Inputs:
        -endpt1, endpt2 (lists of length 2, whose entries are ints)'''
    x1, y1 = endpt1
    x2, y2 = endpt2

    if x1 == x2:
        lb, ub = (min(y1, y2), max(y1, y2))
        points = {Point(x1, this_y) for this_y in range(lb, ub+1)}
    elif y1 == y2:
        lb, ub = (min(x1, x2), max(x1, x2))
        points = {Point(this_x, y1) for this_x in range(lb, ub+1)}
    
    return points

def new_cave(input):
    '''Turn the input into an integer representing the floor of the cave, and
    a set of Point objects representing where the rocks are that block sand.'''
    floor = 0
    paths = []
    for path in input:
        path = path.split(" -> ")
        path = [[int(i) for i in endpt.split(',')] for endpt in path]
        deepest_y = max([endpt[1] for endpt in path])
        if deepest_y > floor:
            floor = deepest_y
        paths.append(path)

    floor += 2 #the floor is 2 units lower than the lowest rock

    blocked = set()
    for path in paths:
        for i in range(len(path) - 1):
            new_blocks = draw(path[i], path[i+1])
            blocked = blocked.union(new_blocks)
    
    return floor, blocked


def run(blocked, part1=True, floor=None):
    cur_grain = Point(500, 0)
    sand_at_rest = 0

    while Point(500, 0) not in blocked:
        at_rest = fall(cur_grain, blocked, floor=floor)
        if at_rest:
            blocked.add(cur_grain)
            sand_at_rest += 1
            cur_grain = Point(500, 0)
        if part1 and cur_grain.y == floor - 1: #grain went "into the abyss"
            return sand_at_rest
    return sand_at_rest

if __name__ == '__main__':
    floor, blocked = new_cave(input)
    print(f"Part 1 answer: {run(blocked, part1=True, floor=floor)}")
    _, blocked = new_cave(input)
    print(f"Part 2 answer: {run(blocked, part1=False, floor=floor)}") #~22sec
    #TODO: Figure out a method that doesn't use as many 'x in set' checks, those
    #get slow quickly
