from aocd import get_data
import networkx as nx

input = [i for i in get_data(day=6, year=2019).split("\n")]


def make_orbit_map(map: list[str]) -> nx.DiGraph:
    """Convert a list of orbits into a map, directed graph representation."""
    G = nx.DiGraph()
    for orbit in map:
        planets = orbit.split(")")
        G.add_edge(planets[1], planets[0])
    return G


def total_orbits_count(G: nx.DiGraph, origin: str) -> int:
    """Count how many direct and indirect orbits there are about a particular
    origin node."""
    orbits = 0
    for node in G.nodes:
        try:
            orbits += nx.shortest_path_length(G, source=node, target=origin)
        except:  # if there is no path between this node and origin, do nothing
            continue
    return orbits


def part1(G: nx.DiGraph) -> int:
    # allow for multiple unconnected orbital systems in one graph
    origins = [node for node in G if G.out_degree(node) == 0]
    total_count = 0
    for origin in origins:
        result = total_orbits_count(G, origin)
        total_count += result
    return total_count


def part2(G: nx.DiGraph) -> int:
    # each of you is only orbiting one planet, so grab that planet from the
    # list of out-edges, which is of length 1 and thus contains one 2-tuple
    you_planet = [p[1] for p in G.out_edges("YOU")][0]
    san_planet = [p[1] for p in G.out_edges("SAN")][0]
    G_prime = G.to_undirected()
    return nx.shortest_path_length(G_prime, source=you_planet, target=san_planet)


if __name__ == "__main__":
    G = make_orbit_map(input)
    print(f"Part 1 solution: {part1(G)}")
    print(f"Part 2 solution: {part2(G)}")
