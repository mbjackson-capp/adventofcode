from aocd import get_data
from typing import Tuple, Set
from copy import deepcopy
from functools import cache

input = get_data(day=17, year=2015)


def parse_input(data: str) -> Tuple[Tuple]:
    return tuple([int(i) for i in data.split("\n")])


@cache
def ways_to_fill(liters: int, containers: Tuple[int | None]) -> Set[Tuple]:
    """Return all unique ways that a tuple of containers of known sizes can
    be filled with n liters of eggnog.
    This takes a few seconds even with cache enabled. TODO: speed up"""
    if liters < 0:
        # Base case: illegal state (you must have overfilled)
        return set()
    elif liters == 0:
        # Base case: exactly full with desired amount
        return {containers}
    else:
        # Recursive step: Try each possible world in which one as-yet-unfilled
        # container is the next to be filled
        result = set()
        for i, container in enumerate(containers):
            if container is not None:
                vol = container
                next_containers = [j for j in deepcopy(containers)]
                # Because order matters if multiple containers have same volume,
                # we must mark this *particular* container full by nulling it
                next_containers[i] = None
                result = result | ways_to_fill(liters - vol, tuple(next_containers))
        return result


def solve(liters: int, data: str) -> int:
    input = parse_input(data)
    ways = ways_to_fill(liters, input)
    p1_ans = len(ways)
    n = 1
    while True:
        # Try to find answers with n containers filled
        n_container_ways = {
            way for way in ways if len([c for c in way if c is None]) == n
        }
        if n_container_ways:
            p2_ans = len(n_container_ways)
            break
        else:
            n += 1
    return p1_ans, p2_ans


if __name__ == "__main__":
    print("Now solving...This may take a few seconds...")
    ans1, ans2 = solve(150, input)
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
