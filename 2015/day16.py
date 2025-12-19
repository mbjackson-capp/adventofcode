from aocd import get_data
import re

# Does this differ between users?
mscam_text = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""


def parse_mscam(mtext: str) -> dict:
    data = {}
    for line in mtext.split("\n"):
        thing, count = line.split(": ")
        count = int(count)
        data[thing] = count
    return data


def parse_sues(sue_text: str) -> dict:
    sues = {}
    for line in sue_text.split("\n"):
        line = line[4:]  # skip 'Sue '
        print(line)
        num, rest = re.split(r"(?<=\d): ", line)
        num = int(num)
        sues[num] = {}
        entries = rest.split(", ")
        for entry in entries:
            thing, count = entry.split(": ")
            count = int(count)
            sues[num][thing] = count
    return sues


def passes_comparision(object_type, mscam_val, sue_val, part=2) -> bool:
    if part == 1:
        return mscam_val == sue_val
    elif object_type in ["cats", "trees"]:
        return mscam_val < sue_val
    elif object_type in ["pomeranians", "goldfish"]:
        return mscam_val > sue_val
    else:
        return mscam_val == sue_val


def solve(data: str, part=1):
    mscam = parse_mscam(mscam_text)
    sues = parse_sues(data)
    for sue, sue_things in sues.items():
        promising = False
        for object, mscam_count in mscam.items():
            if object not in sue_things:
                # I don't remember this Sue having any of this object, but she might
                continue
            if passes_comparision(object, mscam_count, sue_things[object], part=part):
                # This MSCAM result works for this Sue... keep going
                promising = True
            else:
                # this Sue definitely mismatches MSCAM and thus can't be right
                promising = False
                break
        if promising:
            return sue
    raise Exception(
        "Somehow, none of the Sues match the MSCAM results. Debug your code!"
    )


input = get_data(day=16, year=2015)

if __name__ == "__main__":
    print(f"Part 1 answer: {solve(input,part=1)}")
    print(f"Part 2 answer: {solve(input,part=2)}")
