from aocd import get_data
import re


def parse_input(data):
    towels, designs = data.split("\n\n")
    towels = set(towels.split(", "))
    designs = [design for design in designs.split("\n")]
    return towels, designs


towels, designs = parse_input(get_data(day=19, year=2024))
part1_memo = {}
part2_memo = {}


def is_possible(design: str, towels: list[str]):
    """Recursive, memoized function to determine if a design is possible to make
    from a given set of towels. Dynamic programming approach inspired by 'string
    reconstruction' problem; see, e.g. https://people.seas.harvard.edu/~cs125/fall16/lec5.pdf
    """
    if design in part1_memo:
        return part1_memo[design]
    elif design in towels:
        # Alternately, you can initialize part1_memo as {towel: True for towel in towels}
        # outside this function.
        part1_memo[design] = True
        return True
    elif len(design) == 1 and design not in part1_memo:
        part1_memo[design] = False
        return False
    else:
        # e.g. for a string of length 5, should be [(1,4), (2,3), (3,2), (1,4)]
        partitions = [(design[:i], design[i:]) for i in range(1, len(design))]
        for partition in partitions:
            front, back = partition
            if is_possible(front, towels) and is_possible(back, towels):
                part1_memo[design] = True
                return True
        part1_memo[design] = False
        return False


def count_ways_to_make(design, towels):
    """Recursive, memoized function to count how many ways it's possible to make a
    design from a particular set of towels."""
    if design in part2_memo:
        return part2_memo[design]
    if design == "":
        return 1  # vacuously true; always possible to make the empty design
    remove_towel_options = []
    # get all possible options for first towel
    for towel in towels:
        if re.match(f"^{towel}", design):
            remove_towel_options.append(design[len(towel) :])
    # implicit base case: ans is 0 if no valid towel can be taken off front of this design
    ans = sum([count_ways_to_make(option, towels) for option in remove_towel_options])
    part2_memo[design] = ans
    return ans


if __name__ == "__main__":
    part1_count = 0
    part2_count = 0
    print(f"Now running... This could take several seconds...")
    for design in designs:
        if is_possible(design, towels):
            part1_count += 1
            this_count = count_ways_to_make(design, towels)
            part2_count += this_count
    print(f"Part 1 solution: {part1_count}")
    print(f"Part 2 solution: {part2_count}")
