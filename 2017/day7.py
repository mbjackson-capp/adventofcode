from aocd import get_data
from typing import Optional, List
import re
from collections import Counter

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=7, year=2017).split("\n")

ARROW = " -> "


class Disc:
    def __init__(
        self,
        name: str,
        weight: Optional[int] = None,
        parent: Optional[str] = None,
        children: List = [],
    ):
        self.name = name
        self.weight = weight
        self.parent = parent
        self.children = children

    def __repr__(self):
        return (
            f"{self.name} ({self.weight}) -> {[c.name for c in self.children]}"
            if self.children
            else f"{self.name} ({self.weight})"
        )

    @property
    def weight_above(self):
        if self.children == []:
            return self.weight
        else:
            return self.weight + sum([c.weight_above for c in self.children])


def make_tower_nodes(input: List[str]):
    nodes = {}
    for line in input:
        name = re.search(r"^\w+(?=\s)", line).group(0)
        weight = int(re.search(r"\d+", line).group(0))

        if name not in nodes:
            this_node = Disc(name, weight=weight)
            nodes[name] = this_node
        else:
            this_node = nodes[name]
            this_node.weight = weight

        # deal with children
        if len(line.split(ARROW)) >= 2:
            _, child_names = line.split(ARROW)
            child_names = re.split(r",\s?", child_names)
        else:
            child_names = []
        for child in child_names:
            if child not in nodes:
                child_node = Disc(name=child, parent=this_node, children=[])
                nodes[child] = child_node
            else:
                child_node = nodes[child]
                child_node.parent = this_node
            if child_node not in this_node.children:
                # For some reason, "this_node.children.append(child_node)" doesn't work right
                this_node.children = this_node.children + [child_node]

    return nodes


def disc_tower_root(data):
    nodes = make_tower_nodes(data)
    # Get any random node. Why not the first one?
    for actual_node in nodes.values():
        break
    # Recurse up the chain of parents in ~O(log n) time. This lets us have a copy
    # of the disc tower that can be traversed like a tree starting at root node
    while actual_node.parent is not None:
        actual_node = actual_node.parent
    return actual_node


def find_imbalance(tower: Disc, diff: int = 0):
    tower_sums = Counter([c.weight_above for c in tower.children])
    balanced_weight = [k for k, v in tower_sums.items() if v != 1][0]
    try:  # isolate the tower whose weight is different from the others
        imbalanced_weight = [k for k, v in tower_sums.items() if v == 1][0]
    except IndexError:
        # All towers above this one have the same weight, i.e. it's balanced from
        # here on up. So any imbalance below must be because THIS disc is of the
        # wrong weight. This disc's proper weight must make up the gap between
        # its weight and that of the other towers on its same level.
        return tower.weight + diff
    diff = balanced_weight - imbalanced_weight
    for c in tower.children:
        if c.weight_above == imbalanced_weight:
            # Recurse up into the sole tower whose weight does not match others
            return find_imbalance(c, diff=diff)


if __name__ == "__main__":
    tower = disc_tower_root(input)
    print(f"Part 1 answer: {tower.name}")
    p2_ans = find_imbalance(tower)
    print(f"Part 2 answer: {p2_ans}")
