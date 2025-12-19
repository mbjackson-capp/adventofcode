from aocd import get_data
from typing import Tuple
from copy import deepcopy
from functools import cache

input = get_data(day=17, year=2015)


test_input = """20
15
10
5
5"""

test_input2 = """10
5
5"""


def parse_input(data: str) -> Tuple[Tuple]:
    """Because order matters, we need to distinguish specific instances of a
    particular integer; doing that with a 'used flag' boolean bundled with
    each integer"""
    return tuple([(int(i), False) for i in data.split("\n")])


@cache
def ways_to_fill(liters: int, containers: Tuple[Tuple]) -> int:
    if liters < 0:
        # Base case: illegal state (you must have overfilled)
        return set()
    elif liters == 0:
        # Base case: exactly full with desired amount
        return {containers}
    else:
        # Recursive step: Try each possible world in which one yet-unfilled
        # container is filled next
        result = set()
        for i, container in enumerate(containers):
            if container[1] == False:
                vol = container[0]
                next_containers = [i for i in deepcopy(containers)]
                next_containers[i] = (vol, True)
                result = result | ways_to_fill(liters - vol, tuple(next_containers))
        return result


def solve(liters: int, data: str) -> int:
    input = parse_input(data)
    ways = ways_to_fill(liters, input)
    p1_ans = len(ways)
    n = 1
    while True:
        # Try to find answers with n containers filled")
        ways_prime = {way for way in ways if len([c for c in way if c[1] == True]) == n}
        if ways_prime:
            p2_ans = len(ways_prime)
            break
        else:
            n += 1
    return p1_ans, p2_ans


if __name__ == "__main__":
    print("Now solving...This may take a few seconds...")
    ans1, ans2 = solve(150, input)
    print(f"Part 1 answer: {ans1}")
    print(f"Part 2 answer: {ans2}")
