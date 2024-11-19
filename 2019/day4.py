from itertools import groupby

# your input may vary
LOW_END = 108457
HIGH_END = 562042
input = list(range(LOW_END, HIGH_END))


def never_decrease(passwd):
    for i in range(1, 6):
        if int(str(passwd)[i]) < int(str(passwd)[i - 1]):
            return False
    return True


def has_double(passwd):
    for i in range(1, 6):
        if int(str(passwd)[i]) == int(str(passwd)[i - 1]):
            return True
    return False


def part1():
    return [i for i in input if never_decrease(i) and has_double(i)]


def part2_criterion(passwd):
    # Split so string is separated at each boundary between distinct digits
    # e.g. 123444 -> [1, 2, 3, 444]
    splitup = ["".join(grp) for _, grp in groupby(str(passwd))]
    return 2 in [len(i) for i in splitup]


candidates = part1()
print(f"Part 1 solution: {len(candidates)}")

candidates = [i for i in candidates if part2_criterion(i)]
print(f"Part 2 solution: {len(candidates)}")
