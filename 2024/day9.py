from aocd import get_data

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=9, year=2024)


def layoutize(diskmap: str) -> list:
    """Turn a string representation of disk map into a visual layout of files
    and gaps, where each block is an entry in returned list.
    Note that the example in part description (https://adventofcode.com/2024/day/9)
    is misleading: IDs larger than 9 must still take up a *single* block of memory,
    so the layout cannot always be represented as a string in which one character
    represents one block."""
    file_sizes = diskmap[::2]
    ids = {}
    for ix, file in enumerate(file_sizes):
        ids[ix] = int(file)
    gap_sizes = [int(i) for i in diskmap[1::2]]
    blocks = []
    for id in ids.keys():
        for _ in range(ids[id]):
            blocks.append(id)
        try:
            for _ in range(gap_sizes[id]):
                blocks.append(".")
        except IndexError:  # since there are n-1 gaps and n ids
            continue
    return blocks


def first_gap_index(blocks: list, size) -> int:
    """Find the STARTING index of a gap of the desired size."""
    gap_so_far = 0
    in_a_gap = False
    for ix, block in enumerate(blocks):
        if block == ".":
            in_a_gap = True
            gap_so_far += 1
        if in_a_gap and block != ".":
            gap_so_far = 0
            in_a_gap = False
        if gap_so_far == size:
            return ix - size + 1


def checksum(layout):
    chksum = 0
    for i, block in enumerate(layout):
        if block != ".":
            chksum += i * block
    return chksum


def compactify_p1(blocks: list) -> list:
    """Move file blocks one at a time from the end of the disk to the leftmost
    free space block, until there are no gaps remaining between file blocks."""
    while "." in blocks:
        val_to_move = blocks.pop(-1)
        if val_to_move == ".":
            continue
        new_place = first_gap_index(blocks, 1)
        blocks[new_place] = val_to_move
    return blocks


def compactify_p2(blocks: list):
    """Move contiguous files blocks one at a time from the end of the disk to the
    leftmost free space gap large enough to accommodate them, until there are no
    more valid moves possible."""
    file_size = 0
    end_ix = len(blocks) - 1
    while end_ix >= 0:
        if "." not in blocks[:end_ix]:
            break  # can stop early when there are no gaps left to move into
        val_to_move = blocks[end_ix]
        if val_to_move == ".":
            file_size = 0
            end_ix -= 1
            continue
        else:
            file_size += 1
            if blocks[end_ix - 1] == val_to_move:
                end_ix -= 1
                continue  # keep going until you have all blocks of this id
            else:
                new_place = first_gap_index(blocks, file_size)
                if new_place is None:
                    continue
                elif new_place < end_ix:
                    for i in range(file_size):
                        blocks[end_ix + i] = "."
                        blocks[new_place + i] = val_to_move
                    file_size = 0
                else:  # gap comes after this item, not before
                    file_size = 0
                end_ix -= 1
    return blocks


def run(input, part=1):
    layout = layoutize(input)
    compacted = compactify_p1(layout) if part == 1 else compactify_p2(layout)
    return checksum(compacted)


if __name__ == "__main__":
    print(f"Now running Part 1. This may take a few seconds...")
    part1_solution = run(input)
    print(f"Part 1 solution: {part1_solution}")
    print(f"Now running Part 2. This may take a few seconds...")
    part2_solution = run(input, part=2)
    print(f"Part 2 solution: {part2_solution}")
