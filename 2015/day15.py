from aocd import get_data
import re
from itertools import combinations, pairwise
from collections import OrderedDict
from typing import Tuple
from functools import reduce

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=15, year=2015)


def parse_input(data: str) -> dict:
    ingredients = OrderedDict()
    for line in data.split("\n"):
        ingredient, rest = line.split(": ")
        capacity, durability, flavor, texture, calories = [
            int(i) for i in re.findall(r"-?\d+", rest)
        ]
        ingredients[ingredient] = {
            "capacity": capacity,
            "durability": durability,
            "flavor": flavor,
            "texture": texture,
            "calories": calories,
        }
    return ingredients


def stars_and_bars(n: int, k: int):
    """Getting the possible combinations of ingredient amounts can be obtained
    from (more or less reduced to) the 'stars-and-bars' problem in combinatorics:
    If there are n indistinguishable stars and potential containers of width k
    into which they can be placed, treating each space of width 1 between 0 and
    (n + k -1) as contining either a star or a container-demarcating bar,
    return all possible sets of indices of the spaces at which the bars will
    be placed."""
    return combinations(range(n + k - 1), k - 1)


def number_of_each_ingredient(n_cookie: int, k_ingredients: int):
    """Convert outputs of stars-and-bars into actual numbers of each ingredient
    for a cookie of n units and ingredient cabinet with k ingredients in it.
    Idea inspired by https://stackoverflow.com/questions/28965734/general-bars-and-stars;
    implementation my own"""
    assert k_ingredients > 0, "Must have a positive number of ingredients"
    if k_ingredients == 1:
        return [(n_cookie,)]
    bar_indices = stars_and_bars(n_cookie, k_ingredients)
    partitions = []
    for tupl in bar_indices:
        this_partition = []
        left_of_tupl = len(range(0, tupl[0]))
        this_partition.append(left_of_tupl)
        between_sum = 0
        for pair in pairwise(tupl):
            pair_a, pair_b = pair
            between_items = len(range(pair_a, pair_b)) - 1
            this_partition.append(between_items)
            between_sum += between_items
        right_of_tupl = n_cookie - between_sum - left_of_tupl
        this_partition.append(right_of_tupl)
        partitions.append(tuple(this_partition))
    return partitions


def bake_cookie(ingredients: dict, partition: Tuple[int]) -> dict:
    """Return a dictionary representation of a cookie and its numeric properties."""
    zippy = zip(ingredients.items(), partition)
    cookie = {}
    for ing in zippy:
        properties, amt = ing
        prop_dict = properties[1]
        for prop, qty in prop_dict.items():
            if prop not in cookie:
                cookie[prop] = 0
            cookie[prop] += amt * qty
    for prop in cookie:
        if cookie[prop] < 0:
            cookie[prop] = 0
    return cookie


def cookie_properties(cookie: dict) -> int:
    """Obtain the number of calories in a cookie and its cookie score."""
    cals = cookie["calories"]
    del cookie["calories"]
    return cals, reduce(lambda a, b: a * b, cookie.values())


def solve(data: str, part=1):
    """Find the maximum score possible among all legal cookies."""
    ings = parse_input(data)
    options = number_of_each_ingredient(100, len(ings))
    max_score = 0
    for option in options:
        cookie = bake_cookie(ings, option)
        cals, score = cookie_properties(cookie)
        part_bool = True if part == 1 else (cals == 500)
        if part_bool and score > max_score:
            max_score = score
    return max_score


if __name__ == "__main__":
    ings = parse_input(input)
    print(f"Part 1 answer: {solve(input,part=1)}")
    print(f"Part 2 answer: {solve(input,part=2)}")
