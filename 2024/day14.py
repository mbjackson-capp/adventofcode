from aocd import get_data
from dataclasses import dataclass
from math import prod
import numpy as np
import re

np.set_printoptions(linewidth=10000)

input = get_data(day=14, year=2024).split("\n")
WIDTH_X = 101
WIDTH_Y = 103


@dataclass
class Robot:
    p_x: int = 0
    p_y: int = 0
    v_x: int = 0
    v_y: int = 0


def parse_bots(data: list[str]):
    bots = []
    for line in data:
        nums = [int(i) for i in re.findall(r"-?\d+", line)]
        p_x, p_y, v_x, v_y = nums
        bots.append(Robot(p_x, p_y, v_x, v_y))
    return bots


def simulate(bots: list[Robot], seconds: int, max_x=WIDTH_X, max_y=WIDTH_Y):
    for bot in bots:
        bot.p_x = (bot.p_x + (bot.v_x * seconds)) % max_x
        bot.p_y = (bot.p_y + (bot.v_y * seconds)) % max_y
    return bots


def safety_factor(bots: list[Robot], max_x=WIDTH_X, max_y=WIDTH_Y):
    median_x = max_x // 2
    median_y = max_y // 2
    quadrants = {0: [], 1: [], 2: [], 3: []}
    for bot in bots:
        if bot.p_x < median_x and bot.p_y < median_y:
            quadrants[0].append(bot)
        elif bot.p_x < median_x and bot.p_y > median_y:
            quadrants[1].append(bot)
        elif bot.p_x > median_x and bot.p_y < median_y:
            quadrants[2].append(bot)
        elif bot.p_x > median_x and bot.p_y > median_y:
            quadrants[3].append(bot)
    return prod([len(v) for v in quadrants.values()])


def map_bots(bots: list[Robot], max_x=WIDTH_X, max_y=WIDTH_Y):
    arr = np.zeros((max_x, max_y), dtype=int)
    for bot in bots:
        arr[bot.p_x][bot.p_y] += 1
    return arr


def part1(data: str = input):
    bots = parse_bots(data)
    bots = simulate(bots, 100)
    return safety_factor(bots)


def part2(data: str = input, limit=10000):
    TREE_TRUNK = "1 1 1 1 1 1 1 1 1 1 1 1 1"
    bots = parse_bots(data)
    t = 1
    while t < limit:
        bots = simulate(bots, 1)
        for row in map_bots(bots):
            if TREE_TRUNK in str(row):
                return t
        t += 1


if __name__ == "__main__":
    part1_solution = part1()
    print(f"Part 1 solution: {part1_solution}")
    print(
        f"Now running Part 2...This will take a few seconds of real time per 1,000 seconds of simulation..."
    )
    part2_solution = part2()
    print(f"Part 2 solution: {part2_solution}")
