from aocd import get_data
from itertools import permutations
import networkx as nx 
import re

input = get_data(day=9, year=2015).split('\n')


def parse_input(input_lst: list[str]) -> nx.Graph:
    G = nx.Graph()
    for line in input_lst:
        node1, node2, dist = re.split(r' to | = ', line)
        dist = int(dist)
        G.add_edge(node1, node2, weight=dist)
    return G


def delivery_route_lengths(G: nx.Graph) -> list[int]:
    lengths = []
    perms = permutations(G.nodes)
    for perm in perms:
        length = 0
        for ix, node in enumerate(perm):
            if ix < len(perm)-1:
                dist = G[node][perm[ix+1]]['weight']
                length += dist
        lengths.append(length)
    return lengths

if __name__ == '__main__':
    G = parse_input(input)
    lengths = sorted(delivery_route_lengths(G))
    print(f"Part 1 solution: {lengths[0]}")
    print(f"Part 2 solution: {lengths[-1]}")