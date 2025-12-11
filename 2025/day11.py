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


def valid_paths_network(G: nx.DiGraph, source="svr", target="out") -> nx.DiGraph:
    """Prune nodes that aren't on a valid path. This turns out to be useless
    with provided input since every node is on a valid path"""
    toposort = list(nx.topological_sort(G))
    print(f"'dac' at index {toposort.index(DAC)}, 'fft' at index {toposort.index(FFT)}")
    dac_ix = toposort.index(DAC)
    fft_ix = toposort.index(FFT)
    mid_former_ix = min(dac_ix, fft_ix)
    mid_latter_ix = max(dac_ix, fft_ix)
    to_delete = []
    for i, node in enumerate(toposort[:mid_former_ix]):
        if not nx.has_path(G, source, toposort[mid_former_ix]):
            to_delete.append(node)
    for j, node in enumerate(toposort[mid_former_ix:mid_latter_ix]):
        if not nx.has_path(G, source, toposort[mid_latter_ix]):
            to_delete.append(node)
    for node in to_delete:
        G.remove_node(node)
    return G


def part2(G: nx.DiGraph, source: str = "svr", target: str = "out"):
    if nx.has_path(G, DAC, FFT):
        mid_former, mid_latter = (DAC, FFT)
    elif nx.has_path(G, FFT, DAC):
        mid_former, mid_latter = (FFT, DAC)
    else:
        return 0
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
