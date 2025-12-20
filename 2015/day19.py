from aocd import get_data
from typing import Tuple
import re
from functools import cache
import time


test_input1 = """H => HO
H => OH
O => HH

HOH"""

# test_input2 = test_input1 + "OHO"


def parse_input(data: str, reverse=False) -> Tuple[dict, str]:
    rules, molecule = data.split("\n\n")
    rule_dict = {}
    for rule in rules.split("\n"):
        if reverse:
            after, before = rule.split(" => ")
        else:
            before, after = rule.split(" => ")
        if before not in rule_dict:
            rule_dict[before] = after if reverse else [after]
        else:
            rule_dict[before].append(after)
    return rule_dict, molecule


@cache
def possible_replacements(molecule: str, prior: str, repl: str) -> str:
    # Inspired by https://stackoverflow.com/a/55120321
    options = set()
    pattern = re.compile(prior)
    for m in pattern.finditer(molecule):
        before = molecule[: m.start()]
        after = molecule[m.end() :]
        new_molecule = before + repl + after
        options.add(new_molecule)
    return options


def possible_next_molecules(rules: dict, molecule: str) -> set:
    options = set()
    for prior, repls in rules.items():
        for repl in repls:
            options = options | possible_replacements(molecule, prior, repl)
    return options


def part1(data: str) -> int:
    rules, molecule = parse_input(data)
    return len(possible_next_molecules(rules, molecule))


def part2(data: str) -> int:
    """Hypothesis: if we're looking for the minimum number of steps needed to
    create the target molecule from e, the minimum-step process will use the most
    possible big-letter-addition rules in creating the molecule string.
    As such, attempt to run a process "in reverse", greedily undoing a rule that
    creates the most new letters possible within the molecule string, over and over,
    until 'e ' is reached.
    We are "fortunate" in that each reverse-rule end product is unique; this method
    would fail if two forward rules produced the same product on the right hand
    side of the arrow."""
    n_steps = 0
    rules, molecule = parse_input(data, reverse=True)
    prod_lengths = sorted(list({len(k) for k in rules.keys()}), reverse=True)
    while molecule != "e":
        # try to find a substring within the molecule equal to one of the longest
        # products. if that fails, try the second-longest products, then the
        # third-longest, ... etc
        for length in prod_lengths:
            removed_something = False
            long_keys = [k for k in rules.keys() if len(k) == length]
            for long_key in long_keys:
                if removed_something:
                    break
                results = [m for m in re.compile(long_key).finditer(molecule)]
                if results:
                    # run reverse rule at first opportunity to shrink the molecule
                    m = results[0]
                    before = molecule[: m.start()]
                    after = molecule[m.end() :]
                    new_molecule = before + rules[long_key] + after
                    molecule = new_molecule
                    removed_something = True
                    n_steps += 1
                    break
            if removed_something:
                break
    return n_steps


if __name__ == "__main__":
    input = get_data(day=19, year=2015)
    print(f"Part 1 answer: {part1(input)}")
    p2_ans = part2(input)
    print(f"Part 2 answer: {p2_ans}")
