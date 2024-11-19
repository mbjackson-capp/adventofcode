from aocd import get_data
import re

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=7, year=2020).split("\n")


def parse_rules(input) -> dict:
    rules = {}
    for rule in input:
        outer_bag, inner_bag_text = rule.split(" bags contain ")
        inner_bag_text = re.split(r"\sbags?(?:\.|,)\s?", inner_bag_text)[:-1]
        if "no other" in inner_bag_text:
            rules[outer_bag] = {}
        else:
            inner_bags = {}
            for bag_statement in inner_bag_text:
                first_space_idx = re.search(" ", bag_statement).start()
                num = int(bag_statement[:first_space_idx])
                inner_bag = bag_statement[first_space_idx + 1 :]
                inner_bags[inner_bag] = num
            rules[outer_bag] = inner_bags
    return rules


rules = parse_rules(input)


def part1(target_color: str, rules: dict) -> set:
    answers = set()
    outer_bags = []
    for color in rules:
        if target_color in rules[color].keys():
            # get all bags that can IMMEDIATELY contain this bag ("one level up")
            # add them to the set of all colors that work thus far
            outer_bags.append(color)
            answers.update(outer_bags)

    while len(outer_bags) != 0:
        # then do that for the bags you just found, and for the bags you find above those, etc. recursively
        # process terminates when you can't find any more new colors of bag above highest level
        answers.update(part1(outer_bags.pop(), rules))
    return answers


def part2(starting_color: str, rules: dict) -> int:
    if rules[starting_color] == {}:
        return 1  # this bag isn't holding anything
    else:
        return (
            sum(
                [
                    (part2(color, rules) * qty)
                    for color, qty in rules[starting_color].items()
                ]
            )
            + 1  # count this bag!
        )


print(f"Part 1 solution: {len(part1("shiny gold", rules))}")
# subtract 1 because recursive count for part 2 includes the outermost bag
print(f"Part 2 solution: {part2("shiny gold", rules) - 1}")
