from aocd import get_data
import re

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=4, year=2020)
# separate out each passport regardless of line breaks
input = re.sub("\n\n", "|", input)
input = re.sub("\n", " ", input)
input = re.split(r"\|", input)


def passportize(row: str) -> dict:
    passport = {}
    lst = re.split(" ", row)
    for item in lst:
        field, val = re.split(":", item)
        passport[field] = val
    return passport


input = [passportize(row) for row in input]


def is_valid_part1(passport: dict) -> bool:
    ignored_cid = passport.pop("cid", None)
    return len(passport.keys()) == 7


def is_valid_part2(passport: dict) -> bool:
    valid_sum = 0
    for key in passport:
        val = passport[key]
        # due to lazy typing, adds 1 to valid_sum only if boolean evaluates to True
        if key == "byr":
            valid_sum += (len(str(val)) == 4) and (1920 <= int(val) <= 2002)
        elif key == "iyr":
            valid_sum += (len(str(val)) == 4) and (2010 <= int(val) <= 2020)
        elif key == "eyr":
            valid_sum += (len(str(val)) == 4) and (2020 <= int(val) <= 2030)
        elif key == "hgt":
            valid_sum += (
                (len(str(val)) == 5)
                and (val[-2:] == "cm")
                and (150 <= int(val[:3]) <= 193)
            ) or (
                (len(str(val)) == 4)
                and (val[-2:] == "in")
                and (59 <= int(val[:2]) < 76)
            )
        elif key == "hcl":
            valid_sum += (len(str(val)) == 7) and val[0] == "#"
        elif key == "ecl":
            valid_sum += val in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        elif key == "pid":
            valid_sum += (str(val).isnumeric()) and (len(str(val)) == 9)

    return valid_sum == 7


def validate_all():
    valid_part1 = 0
    valid_part2 = 0
    for passport in input:
        # use boolean trick again: int + True == int + 1
        valid_part1 += is_valid_part1(passport)
        valid_part2 += is_valid_part2(passport)
    return valid_part1, valid_part2


if __name__ == "__main__":
    ans1, ans2 = validate_all()
    print(f"Solution to part 1: {ans1}")
    print(f"Solution to part 2: {ans2}")
