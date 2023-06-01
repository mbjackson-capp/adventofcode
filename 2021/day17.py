from aocd import get_data
# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re

# Problem statement: https://adventofcode.com/2021/day/17

input = [int(i) for i in re.findall(r'[-\d]+', get_data(day=17, year=2021))]

class Probe:
    def __init__(self, x_vel=0, y_vel=0):
        self.x_pos = 0
        self.y_pos = 0
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.y_max = 0
        self.step = 0

    def update(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.y_max = max(self.y_pos, self.y_max)
        if self.x_vel != 0: # drag
            self.x_vel = self.x_vel -1 if self.x_pos > 0 else self.x_vel + 1
        self.y_vel -= 1     # gravity
        self.step += 1

    def __repr__(self):
        '''For debugging'''
        return (f'Pos: {self.x_pos, self.y_pos}, Vel: {self.x_vel, self.y_vel} ' +
                f'Step: {self.step}, y_max: {self.y_max}')


def launch(start_xvel, start_yvel, target:list):
    '''Simulate a Probe launch. 
    Returns: maximum height reached by the Probe if target is hit'''
    assert len(target) == 4 and target == [int for int in target]
    x_lb, x_ub, y_lb, y_ub = target
    p = Probe(start_xvel, start_yvel)
    while not stopping_condition(p, target):
        p.update()
        if p.x_pos in range(x_lb, x_ub+1) and p.y_pos in range(y_lb, y_ub+1):
            return p.y_max

def stopping_condition(p: Probe, target):
    x_lb, x_ub, y_lb, _ = target
    return ((sign(p.x_vel) not in (0, sign(x_lb))) or # Probe going wrong way
       (sign(p.y_vel) < 0 and p.y_pos < y_lb) or      # below target and falling
       (p.x_pos > x_ub))                              # past target

def sign(int):
    try:
        return int / abs(int)
    except ZeroDivisionError:
        return 0

def min_xstart(x_lb):
    '''Find the lowest x-velocity at which the Probe will overcome drag to hit
    the leftmost bound of the target.'''
    x_start = 0
    while True:
        if sum(range(x_start+1)) >= x_lb:
            return x_start
        x_start += 1

def run(input): 
    hits = 0
    y_max = 0
    x_lb, x_ub, y_lb, _ = input
    # starting x velocity can't be faster than edge of target
    for x in range(min_xstart(x_lb), x_ub+1):
        # starting y velocity of y_lb could hit target in one step
        # upon inspection, Probe hits w/ max height when starting y-velocity is 
        # sign-flipped y_lb-1. TODO: use a helper function to verify
        for y in range(y_lb, -y_lb):
            result = launch(x, y, input)
            if result is not None:
                hits += 1
                if result > y_max:
                    y_max = result
    print(f"Part 1 answer: {y_max}")
    print(f"Part 2 answer: {hits}")


if __name__ == '__main__':
    run(input)