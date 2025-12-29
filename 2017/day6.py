from aocd import get_data
import re
from typing import List

input = [int(i) for i in re.split(r"\s+", get_data(day=6, year=2017))]


def index_to_redistribute_from(banks: List[int]) -> int:
    return min([i for i, blocks in enumerate(banks) if blocks == max(banks)])


def do_redistribution(banks: List[int]) -> List[int]:
    bank_ix = index_to_redistribute_from(banks)
    blocks_to_distribute = banks[bank_ix]
    banks[bank_ix] = 0
    for block in range(blocks_to_distribute):
        bank_ix = (bank_ix + 1) % len(banks)
        banks[bank_ix] += 1
    return banks


def solve(banks: List[int]) -> int:
    cycles = 0
    seen = {}
    while True:
        banks = do_redistribution(banks)
        cycles += 1
        if tuple(banks) not in seen:
            seen[tuple(banks)] = cycles
        else:
            cycle_len = cycles - seen[tuple(banks)]
            break
    return cycles, cycle_len


if __name__ == "__main__":
    p1_ans, p2_ans = solve(input)
    print(f"Part 1 answer: {p1_ans}\nPart 2 answer: {p2_ans}")
