import networkx as nx
from aocd import get_data
from math import sqrt
from tqdm import tqdm

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/8

input = get_data(day=8, year=2025)


def make_junction_boxes(data: str) -> nx.Graph:
    data = [[int(j) for j in i.split(",")] for i in data.split("\n")]
    G = nx.Graph()
    for i, box in enumerate(data):
        x, y, z = box
        G.add_node(i, name=f"{x},{y},{z}", x=x, y=y, z=z)
    return G


def euclidean_distance(node1, node2) -> float:
    node1 = node1[1]
    node2 = node2[1]
    return sqrt(
        (node1["x"] - node2["x"]) ** 2
        + (node1["y"] - node2["y"]) ** 2
        + (node1["z"] - node2["z"]) ** 2
    )


def make_edge_specs(G: nx.Graph):
    edge_specs = []
    for i, node1 in enumerate(list(G.nodes(data=True))):
        for j, node2 in enumerate(list(G.nodes(data=True))):
            # clunky way to ensure that i and j match node ids
            if i <= j:
                continue
            dist = euclidean_distance(node1, node2)
            edge_link = (i, j)
            edge_specs.append((edge_link, dist))
    edge_specs = sorted(edge_specs, key=lambda x: x[1])
    return edge_specs


def connect_circuits(G: nx.Graph, stop_after: int | None = None):
    """Consider all potential edges, then add edges to connect boxes into circuits.
    If stop_after is defined, stop after that many edges have been CONSIDERED.
    (This is the proper way to interpret suboptimal wording of Part 1 problem
    statement.)
    Returns G, the graph with edges. For part 2 / when there's no arbitrary
    number of potential edges to stop after, also returns the X coordinates
    of the nodes connected by the final edge. (Note that when Part 2 runs all
    the way through, it is basically an implementation of Kruskal's algorithm
    for finding a minimum spanning tree."""
    edge_specs = make_edge_specs(G)
    for i, es in tqdm(enumerate(edge_specs)):
        if stop_after is not None and i >= stop_after:
            break
        node_id1, node_id2 = es[0]
        if node_id1 not in nx.node_connected_component(G, node_id2):
            G.add_edge(node_id1, node_id2)
        # circuits are trees in the graph theoretic sense, so there can be at
        # most n-1 edges between n nodes. Therefore, once the last possible edge
        # has been made, you can break immediately and know exactly what the
        # X values of its nodes are
        if len(list(G.edges)) == len(list(G.nodes)) - 1:
            final_x1 = G.nodes[node_id1]["x"]
            final_x2 = G.nodes[node_id2]["x"]
            return G, final_x1, final_x2
    return G, None, None


def part1(data: str, stop_after=10):
    G = make_junction_boxes(data)
    G, _, _ = connect_circuits(G, stop_after=stop_after)
    circuit_sizes = sorted(
        [len(c) for c in list(nx.connected_components(G))], reverse=True
    )
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def part2(data: str):
    G = make_junction_boxes(data)
    G, final_x1, final_x2 = connect_circuits(G)
    return final_x1 * final_x2


if __name__ == "__main__":
    ans1 = part1(input, stop_after=1000)
    print(f"Part 1 answer: {ans1}")
    ans2 = part2(input)
    print(f"Part 2 answer: {ans2}")
