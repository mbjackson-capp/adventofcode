from aocd import get_data
import networkx as nx
import numpy as np
from utils import gridify, neighbor_locs, manhattan_dist


def pathfind(arr: np.array) -> nx.DiGraph:
    """Turn an array representing the racetrack into a (linear) directed graph
    so that future calculations can be done graph-theoretically rather than
    geometrically. Uses a breadth-first search-esque approach."""
    start = tuple(int(i[0]) for i in np.where(arr == "S"))
    end = tuple(int(i[0]) for i in np.where(arr == "E"))
    arr[end] = "."
    G_track = nx.DiGraph()
    path = [start]
    while end not in path:
        curr_x, curr_y = path[-1]
        next = [
            pt
            for pt in neighbor_locs(arr, curr_x, curr_y)
            if (arr[pt] == ".") and (pt not in path)
        ]
        assert (
            len(next) == 1
        ), f"Somehow there are {len(next)} paths ahead instead of one"
        path.append(next[0])
    G_track.add_nodes_from(path)
    for ix, pt in enumerate(path):
        try:
            G_track.add_edge(pt, path[ix + 1], weight=1)
        except IndexError:  # the last node doesn't have a node after it
            break
    return G_track, start, end


def get_valid_cheats(G_track: nx.DiGraph, max_cheat_len=2) -> dict:
    """Check each spot in the racetrack to find all potential cheats whose
    path length is of maximum allowable length or shorter. Track the amount
    of time saved by each valid cheat path discovered, then return a Counter-like
    of how many paths existed that saved each particular amount of time.

    Runtime complexity is Theta(V^2), where V is the number of vertices (spots
    in the racetrack)."""
    savings_ctr = {}
    for i, node_a in enumerate(G_track.nodes):
        # start looking two nodes ahead
        for j, node_b in enumerate(list(G_track.nodes)[i + 2 :]):
            mdist = manhattan_dist(node_a, node_b)
            if 2 <= mdist <= max_cheat_len:
                # We can save time because we know node_a and node_b are j+2 apart;
                # i.e. j+2 == nx.shortest_path_length(G_track, node_a, node_b)
                savings = (j + 2) - mdist
                if savings <= 0:
                    continue
                if savings not in savings_ctr:
                    savings_ctr[savings] = 0
                savings_ctr[savings] += 1
    return savings_ctr


def run(G_track, cheat_len=2):
    print(
        f"Getting savings from cheats of length <= {cheat_len}. This could take a few seconds..."
    )
    savings_ctr = get_valid_cheats(G_track, max_cheat_len=cheat_len)
    solution = sum([v for k, v in savings_ctr.items() if k >= 100])
    return solution


if __name__ == "__main__":
    input = get_data(day=20, year=2024)
    print(f"Gridifying input...")
    input = gridify(input)
    print(f"Pathfinding original path. This could take a few seconds...")
    G_track, start, end = pathfind(input)

    part1_solution = run(G_track)
    print(f"Part 1 solution: {part1_solution}")

    part2_solution = run(G_track, cheat_len=20)
    print(f"Part 2 solution: {part2_solution}")
