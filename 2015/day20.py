from aocd import get_data
from typing import Set
from math import sqrt, ceil
from functools import cache

# NOTE: Unfortunately for us, there is no efficient way to get all of a number's
# integer divisors, and the sum of all an integer's divisors (the 'aliquot sum'
# of n plus n itself) is not a well-behaved function, in part because the
# distribution of primes is unknown ex ante. This file thus uses a naive brute
# force method. TODO: find improvements.


@cache
def all_divisors(n: int, up_to_multiple: int | None = None) -> Set[int]:
    """Relatively slow and non-recursive naive trial division method for finding
    all divisors of an integer. If up_to_multiple keyword is defined, keep
    the divsior only if the integer is less than or equal to that multiple
    of the divisor (which will be 50 in Part 2)."""
    result = {1, n}
    for trial in range(2, ceil(sqrt(n)) + 1):
        if n / trial == int(n / trial):
            if up_to_multiple is None or n <= up_to_multiple * trial:
                result.add(trial)
            if up_to_multiple is None or n <= up_to_multiple * (n / trial):
                result.add(n / trial)
    return result


def num_presents(nth_house: int, part=1) -> int:
    multiplier = 11 if part == 2 else 10
    up_to_multiple = 50 if part == 2 else None
    return multiplier * sum(all_divisors(nth_house, up_to_multiple=up_to_multiple))


def solve(target: int, part=1):
    nth_house = 10  # can skip the first 9; we know those fail from problem text
    while True:
        # can't do straight binary search because the boolean
        # (num_presents(x-1) < num_presents(x) < num_presents(x+1)) is not always True.
        # TODO: consider a variant of binary search where an arbitrary high number
        # is found, then if its num_presents > target, check the numbers 1/2,
        # 3/4, 7/8 etc of the way to that number; if one of those has num_presents
        # > target, make that the new upper bound and check the same ratios to it...
        # issue is that in the worst case you may still have to check every number
        np = int(num_presents(nth_house, part=part))
        if np >= target:
            return nth_house
        else:
            nth_house += 1


if __name__ == "__main__":
    target = int(get_data(day=20, year=2015))
    print("Now solving Part 1...this may take a minute...")
    print(f"Part 1 answer: {solve(target, part=1)}")
    print(f"Now solving Part 2...This could take a minute...")
    print(f"Part 2 answer: {solve(target, part=2)}")
