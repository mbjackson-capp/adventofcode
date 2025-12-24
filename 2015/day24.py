from aocd import get_data
from typing import List
from math import prod
from itertools import chain, combinations
from tqdm import tqdm


def packageize(data: str) -> frozenset[int]:
    return frozenset({int(i) for i in data.split("\n")})


def powerset(iterable):
    "Subsequences of the iterable from shortest to longest."
    "Source: https://docs.python.org/3/library/itertools.html#itertools-recipes"
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def valid_containers(packages: List[int]):
    # takes about 2 minutes to get through input of provided size
    target_p1 = sum(packages) // 3
    target_p2 = sum(packages) // 4
    valids = {3: [], 4: []}
    all_options = powerset(packages)
    for option in tqdm(all_options):
        if sum(option) == target_p1:
            valids[3].append(option)
        if sum(option) == target_p2:
            valids[4].append(option)
    return valids


def min_quantum_entanglement(valids: dict, part=1) -> int:
    # TODO: is this guaranteed to work? we could get a small container that
    # somehow doesn't allow for constructing the other containers we need
    # for the sleigh to be balanced.
    # Counterexample from Reddit: say you have packages [1, 5, 9]. the sleigh
    # can't be constructed. (let's assume from problem text that inputs will
    # always work for both parts)
    # TODO: implement some check that the smallest length allows for constructing
    # a full sleigh
    vcs = valids[3] if (part == 1) else valids[4]
    min_qes_by_len = {}
    for vc in vcs:
        if len(vc) not in min_qes_by_len:
            min_qes_by_len[len(vc)] = float("inf")
        vc_prod = prod(vc)
        if vc_prod < min_qes_by_len[len(vc)]:
            min_qes_by_len[len(vc)] = vc_prod
    min_len = min(min_qes_by_len.keys())
    return min_qes_by_len[min_len]


if __name__ == "__main__":
    input = get_data(day=24, year=2015)
    packages = packageize(input)
    print(
        f"Getting all valid container contents for both parts...May take a minute or two..."
    )
    valids = valid_containers(packages)
    print(f"Part 1 answer: {min_quantum_entanglement(valids, part=1)}")
    print(f"Part 2 answer: {min_quantum_entanglement(valids, part=2)}")
