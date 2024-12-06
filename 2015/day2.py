from aocd import get_data

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = [i.split("x") for i in get_data(day=2, year=2015).split("\n")]
input = [[int(i) for i in box] for box in input]


def part1():
    total_paper = 0
    for box in input:
        l, w, h = box
        sides = [l * w, w * h, l * h]
        wrapping_paper = sum([2 * side for side in sides]) + min(sides)
        total_paper += wrapping_paper
    return total_paper


def part2():
    total_ribbon = 0
    for box in input:
        l, w, h = box
        perimeters = [2 * (l + w), 2 * (w + h), 2 * (l + h)]
        box_ribbon = min(perimeters)
        bow = l * w * h
        total_ribbon += box_ribbon + bow
    return total_ribbon


print(f"Part 1 solution: {part1()}")
print(f"Part 2 solution: {part2()}")
