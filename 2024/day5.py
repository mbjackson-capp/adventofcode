from aocd import get_data
import networkx as nx
from itertools import pairwise, permutations
from collections import Counter

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
# Problem statement: https://adventofcode.com/2024/day/4

rules, updates = get_data(day=5, year=2024).split("\n\n")
rules = [tuple([int(i) for i in rule.split("|")]) for rule in rules.split("\n")]
updates = [[int(u) for u in updt.split(",")] for updt in updates.split("\n")]


def graph_from_rules(rules) -> nx.DiGraph:
    G = nx.DiGraph()
    G.add_edges_from(rules)
    return G


def assess_validities(G: nx.DiGraph, rules, updates: list[int]):
    valid_updates = []
    invalid_updates = []
    for update in updates:
        links = list(pairwise(update))
        update_legal = True
        for link in links:
            src, trgt = link
            if not G.has_edge(src, trgt):
                update_legal = False
                invalid_updates.append(update)
                break
        if update_legal:
            valid_updates.append(update)

    return valid_updates, invalid_updates


def solve(updates_list: list[int]) -> int:
    middles = [update[len(update) // 2] for update in updates_list]
    return sum(middles)


def part1(rules, updates):
    G = graph_from_rules(rules)
    valid_updates, _ = assess_validities(G, rules, updates)
    return solve(valid_updates)


def part2(rules, updates):
    G = graph_from_rules(rules)
    _, invalid_updates = assess_validities(G, rules, updates)
    reordered = []
    for update in invalid_updates:
        reordered.append(reorder(rules, update))
    return solve(reordered)


def reorder(rules, update: list[int]):
    """Find the proper ordering for an out-of-order update by looking at all
    relevant rules and seeing how many of such rules each number in the update
    is on the left-hand side for (since a number on the left-hand side of more
    rules has to be further to the left in a final ordering)"""
    perms = [perm for perm in permutations(update, 2) if perm in rules]
    ctr = Counter([p[0] for p in perms])
    # There is one number left over that isn't on the left of any relevant rule,
    # i.e. that has to come last
    last = [p[1] for p in perms if p[1] not in ctr][0]
    ctr[last] = 0
    reordered = sorted(update, key=lambda x: ctr[x], reverse=True)
    return reordered


part1_solution = part1(rules, updates)
print(f"Part 1 solution: {part1_solution}")

part2_solution = part2(rules, updates)
print(f"Part 2 solution: {part2_solution}")
