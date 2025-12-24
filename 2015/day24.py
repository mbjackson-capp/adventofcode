from aocd import get_data
from functools import cache
from typing import List, Set
from copy import deepcopy
from math import prod


simple_test = """1
2
3
4
5"""

test_input = """1
2
3
4
5
7
8
9
10
11"""

test_input2 = """1
2
3
7
11
13
17
19
23
31
37"""

"""NOTES

We need to do three things:
- 1) Find all valid assignments of the packages into 3 components of exactly equal weight (=sum)
- 2) Isolate the assignments in which Group 1 is the smallest 
- 3) calculate the QE (=product) of each Group 1, keeping only the minimum

Observations:
- It doesn't actually matter what the order of the packages is right now, we can just declare
the smallest one to be Group 1 after the fact
- It also doesn't matter the order of packages within a compartment, so compartments should
be represented by sets rather than lists or tuples
- Step 1 will almost certainly have to be done recursively, considering each new possible
world where one of the remaining packages is assigned to one of the remaining available comparments
- you can calculate the target weight ahead of time and skip over trying containers that have already
hit that weight
- The return type is like Set[Set[Set[int]]]
- if you try to functools @cache this you'll hit "unhashable type list" unless the remaining
containers are amde tuples. 
    - bad news: set is ALSO unhashable
    - bad news: you can't even have a set of sets without running into TypeError: unhashable type 'set'
    - you can use frozensets but uh they're frozen
- you might want to make this flexible enough to have a number of containers other than 3; 
very posible that part 2 is like "suprise, there are actually 5 containers" or whatever

For example if input is [1,2,3,4,5], one possible recursive tree call branch ends in
{ { {1,4}, {3,2}, {5} } }
actually all other valid branches end in equivalents of this, so you'd end up with like
{ { {1,4}, {3,2}, {5} } } | { { {4,1}, {5}, {2,3} } } == { { {1,4}, {3,2}, {5} } }

Base case FAIL: there are no packages left to assign and the compartments are of unequal weight
(let's try to make sure this never happens)
    return empty set (no sets of 3 compartments are possible)
Base case FAIL: there are packages left to assign, but a remaining package is so heavy
that it would overfill any compartment it is put in
    return empty set
Base case FAIL: any compartment is already overfilled
    return empty set
Base case GOOD: there are no packages left to assign and every compartment is of equal weight
    return set of one set of these three compartments

    
Recursive step: Consider the list of remaining packages and the current state of the
containers.
For package in remaining packages:
    Try putting it in container 1, call this function on new containers and list without this package
    same but container 2
    same but container 3
Union together the result of ALL calls you just made

"""


def packageize(data: str) -> frozenset[int]:
    return frozenset({int(i) for i in data.split("\n")})


# Let's do a shitty listy version and then reformat for @cache
def valid_sleighs(packages: frozenset[int], n_containers: int = 3):
    containers = tuple(frozenset() for _ in range(n_containers))
    # containers = frozenset({frozenset() for _ in range(n_containers)})
    target = sum(packages) // n_containers
    print(f"We want a weight of {target} in each of {n_containers} containers. Go!")
    return valid_sleigh_helper(packages, target, containers=containers)


# frozenset({frozenset({4, 5}), frozenset({2, 3})}) == frozenset({frozenset({2, 3}), frozenset({4, 5})})
# that's what I want to avoid unhashable type issues

# NOTE: in all provided inputs, the package weights are unique, so packages can be a frozenset too
# and thus this becomes hashable and thus memoizable. let's see if that's enough


# okay, even with @cache it takes ~5-6 for n=9 packages
# and that goes up to ~10-12 seconds for n=10 packages.
# we got exponential runtime still
@cache
def valid_sleigh_helper(
    packages: frozenset[int], target: int, containers
) -> Set[frozenset[frozenset[int]]]:
    # print(packages, target, containers)
    # the returns aren't changing so those can be frozensets
    # Base case: a container is overfull
    if any(sum(c) > target for c in containers):
        print(f"Overfull container among {containers}")
        return set()
    # Base cases: No packages left
    if len(packages) == 0:
        if all(sum(c) == target for c in containers):
            print(f"No packages left and {containers} is valid! Append to response")
            print(containers)
            return {frozenset(frozenset(c) for c in containers)}
        else:  # this should never happen
            raise ValueError(f"No packages left and {containers} should never happen")
    # Recursive step: Consider each way to add one package to any one of the
    # containers
    # print("Recurse down")
    result = set()
    for package in packages:
        for j, container in enumerate(containers):
            new_packages = frozenset({p for p in packages if p != package})
            new_containers = list(containers)
            new_containers[j] = frozenset(container | {package})
            if sum(new_containers[j]) <= target:
                new = valid_sleigh_helper(new_packages, target, tuple(new_containers))
                result = result | new
    return result


def quantum_entanglement(package_config) -> int:
    min_len_so_far = float("inf")
    for s in package_config:
        if min(len(subset) for subset in s) < min_len_so_far:
            min_len_so_far = min(len(subset) for subset in s)
    qe = float("inf")
    for s in package_config:
        if min(len(subset) for subset in s) == min_len_so_far:
            this_qe = min(prod(subset) for subset in s if len(subset) == min_len_so_far)
            if this_qe < qe:
                qe = this_qe
    return qe


input = get_data(day=24, year=2015)
if __name__ == "__main__":
    simple_packages = packageize(test_input)
    result = valid_sleighs(simple_packages)
    for s in result:
        print(s)
    print(quantum_entanglement(result))
