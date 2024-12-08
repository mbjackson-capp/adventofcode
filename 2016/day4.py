from aocd import get_data
import re
from collections import Counter

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2016/day/4

input = get_data(day=4, year=2016).split("\n")
SUBCOMPONENTS_RE = r"[a-z\-]+(?=\d)|\d+|(?<=\[)[a-z]{5}(?=\])"


def sector_id_if_valid(line: str):
    encrypted_name, sector_id, checksum = re.findall(SUBCOMPONENTS_RE, line)
    ctr = Counter(encrypted_name)
    del ctr["-"]
    top_5 = sorted(
        [(k, v) for k, v in ctr.items()],
        key=lambda pair: (ctr[pair[0]], -ord(pair[0])),
        reverse=True,
    )
    top_5 = [pair[0] for pair in top_5][:5]
    correct_checksum = "".join(top_5)
    if checksum == correct_checksum:
        return int(sector_id)
    return 0


def part1():
    count = 0
    real_rooms = []
    for line in input:
        count += sector_id_if_valid(line)
        real_rooms.append(line)
    return count, real_rooms


def decrypt_room_name(room):
    encrypted_name, sector_id, _ = re.findall(SUBCOMPONENTS_RE, room)
    sector_id = int(sector_id)
    # ord("a") == 97, ord("b") == 98, etc. subtract down for offset so that
    # continuous Caesar shift will work properly on a = 0,  b = 1, ... z = 25
    ORD_OFFSET = 97
    ALPHABET_LENGTH = 26
    decrypted_name = []
    for word in encrypted_name.split("-"):
        alphabet_indices = [ord(ltr) - ORD_OFFSET for ltr in word]
        indices_shifted = [
            (ix + sector_id) % ALPHABET_LENGTH for ix in alphabet_indices
        ]
        decrypted_word = "".join([chr(ltr + ORD_OFFSET) for ltr in indices_shifted])
        decrypted_name.append(decrypted_word)
    return " ".join(decrypted_name).strip(), sector_id


if __name__ == "__main__":
    part1_solution, part2_rooms = part1()
    print(f"Part 1 solution: {part1_solution}")
    DESIRED_ROOM = "northpole object storage"  # revealed by inspecting decrypted names
    for room in part2_rooms:
        decrypted_name, this_sectorid = decrypt_room_name(room)
        if decrypted_name == DESIRED_ROOM:
            break
    print(f"Part 2 solution: {this_sectorid}")
