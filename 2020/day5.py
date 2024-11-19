from aocd import get_data
import re
from math import floor, ceil

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=5, year=2020).split("\n")


def binary_search(lo, hi, str):
    if lo == hi or str == "":
        return lo
    else:
        mid = floor((lo + hi) / 2)
        if str[0] in "BR":
            lo = mid + 1
        elif str[0] in "FL":
            hi = mid
        return binary_search(lo, hi, str[1:])


def decode(bpass: str) -> tuple[int, int, int]:
    ROW_COL_BREAK = 7
    row = binary_search(0, 127, bpass[:ROW_COL_BREAK])
    col = binary_search(0, 7, bpass[ROW_COL_BREAK:])
    seat_id = (row * 8) + col
    return row, col, seat_id


def main():
    decoded_bpasses = []
    max_id = 0
    for bpass in input:
        decoded = decode(bpass)
        decoded_bpasses.append(decoded)
        this_id = decoded[2]
        if this_id > max_id:
            max_id = this_id
    print(f"Part 1 solution: {max_id}")

    # sort all passes by ID number ascending
    decoded_bpasses = sorted(decoded_bpasses, key=lambda x: x[2])
    last_id_seen = None
    for i, bpass in enumerate(decoded_bpasses):
        this_id = bpass[2]
        if i != 0 and this_id != last_id_seen + 1:
            print(f"Part 2 solution: {this_id - 1}")
            break
        else:
            last_id_seen = this_id


if __name__ == "__main__":
    main()
