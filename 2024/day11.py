from aocd import get_data
from collections import Counter
from datetime import datetime

input = [int(i) for i in get_data(day=11, year=2024).split(" ")]


# NAIVE APPROACH -- runtime scales exponentially with the number of blinks,
# i.e, ~ O(2^b). Bogs down seriously by about 40 blinks.


def apply_rules(stone: int) -> int:
    if stone == 0:
        return 1
    if len(str(stone)) % 2 == 0:
        divider = len(str(stone)) // 2
        left_stone = int(str(stone)[:divider])
        right_stone = int(str(stone)[divider:])
        return left_stone, right_stone
    else:
        return stone * 2024


def blink(stones: list[int]) -> list[int]:
    results = []
    for stone in stones:
        this_result = apply_rules(stone)
        if type(this_result) == int:
            results.append(this_result)
        else:
            results += this_result
    return results


def run(stones: list[int], num_blinks=25):
    ans = 0
    for b in range(num_blinks):
        stones = blink(stones)
        ans = len(stones)
    return ans


"""
Notice some patterns are predictable:
0 -> 
1 -> 
2024 -> 
20, 24 -> 
2, 0, 2, 4 -> 
4048, 1, 4048, 8096 ->
40, 48, 2024, 40, 48, 80, 96...
While instructions stress that stones stay in the same order, their order 
doesn't *actually* seem to matter to the total count. (AoC 2021 day6
lanternfish reproduction rules are similar: since ultimate pattern is repetitious,
and individuals are indistinguishable w/r/t how they contribute to the final answer,
you don't need to track individuals.)
"""

# IMPROVED APPROACH - runtime scales much more sanely; can do thousands of blinks
# in seconds


def run_faster(stones: list[int], num_blinks=25):
    ctr = Counter(stones)
    for _ in range(num_blinks):
        new_ctr = {}
        for old_stone, old_count in ctr.items():
            new_stones = []
            if old_stone == 0:
                new_stones.append(1)
            elif len(str(old_stone)) % 2 == 0:
                divider = len(str(old_stone)) // 2
                left_stone = int(str(old_stone)[:divider])
                new_stones.append(left_stone)
                right_stone = int(str(old_stone)[divider:])
                new_stones.append(right_stone)
            else:
                new_stones.append(old_stone * 2024)

            for new_stone in new_stones:
                if new_stone not in new_ctr.keys():
                    new_ctr[new_stone] = 0
                new_ctr[new_stone] += old_count
        ctr = new_ctr
    return sum(new_ctr.values())


if __name__ == "__main__":
    part1_solution_old = run(input, 25)
    part1_solution_new = run_faster(input, 25)
    assert part1_solution_old == part1_solution_new
    print(f"Part 1 solution: {part1_solution_new}")

    part2_solution = run_faster(input, 75)
    print(f"Part 2 solution: {part2_solution}")
