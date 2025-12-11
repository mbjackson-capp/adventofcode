from aocd import get_data
import networkx as nx
import matplotlib.pyplot as plt
from functools import cache


# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/11

DAC = "dac"
FFT = "fft"


def parse_input(data: str) -> nx.DiGraph:
    G = nx.DiGraph()
    for line in data.split("\n"):
        source, targets = line.split(": ")
        targets = targets.split(" ")
        for target in targets:
            G.add_edge(source, target)
    return G


def draw_network(G, filepath: str) -> None:
    """Create an image of the network and save to folder. For debug purposes only;
    wraps around pretty basic matplotlib and networkx functionality"""
    fig = plt.figure(figsize=(40, 18))
    ax = plt.subplot(111)
    ax.set_title("Advent of Code 2025 Day 11 Visualization", fontsize=10)

    pos = nx.bfs_layout(G, start="svr")
    nx.draw(
        G,
        pos,
        node_size=200,
        node_color="#9999FF",
        font_size=8,
        with_labels=True,
    )

    # plt.tight_layout()
    plt.savefig(filepath, format="PNG")
    print(f"Drawing saved to {filepath}")


@cache
def num_paths_between(G: nx.DiGraph, source, target) -> int:
    # Base case: no paths exist (networkx can check this quickly)
    if not nx.has_path(G, source, target):
        return 0
    # Base case: there is trivially a 0-edge path from this node to itself
    if source == target:
        return 1
    # Recursive step: add together the number of paths into each of this node's
    # immediate predecessors. (Incorporates the base case where source has no
    # in-edges and thereby returns 0)
    else:
        precursors = [e[0] for e in G.in_edges(target)]
        return sum(
            [num_paths_between(G, source, precursor) for precursor in precursors]
        )


def part2(G: nx.DiGraph, source: str = "svr", target: str = "out"):
    # determine which of 'dac' or 'fft' must come first in valid paths
    toposort = list(nx.topological_sort(G))
    mid_former, mid_latter = (
        (DAC, FFT) if toposort.index(DAC) < toposort.index(FFT) else (FFT, DAC)
    )
    return (
        num_paths_between(G, source, mid_former)
        * num_paths_between(G, mid_former, mid_latter)
        * num_paths_between(G, mid_latter, target)
    )


if __name__ == "__main__":
    input = get_data(day=11, year=2025)
    G = parse_input(input)
    print(f"Part 1 answer: {num_paths_between(G, "you", "out")}")
    print(f"Part 2 answer: {part2(G)}")
