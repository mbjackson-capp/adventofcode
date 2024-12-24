from aocd import get_data
from itertools import combinations
import networkx as nx


def parse_input(data):
    G = nx.Graph()
    tees = set()
    for line in data.split('\n'):
        node1, node2 = line.split('-')
        G.add_edge(node1, node2)
        if node1[0] == 't':
            tees.add(node1)
        if node2[0] == 't':
            tees.add(node2)
    return G, tees


def part1(input):
    G, tees = parse_input(input)
    t_threes = set()
    for t_node in tees:
        t_neighbor_options = list(combinations(G.neighbors(t_node), 2))
        for comb in t_neighbor_options:
            comb_a, comb_b = comb
            if G.has_edge(comb_a, comb_b): # triangle is complete
                t_threes.add(''.join(sorted([t_node, comb_a, comb_b])))
    return G, len(t_threes)

def part2(G: nx.Graph) -> str:
    # Note: the requirement from Part 1 that a computer whose name starts with 't'
    # has to be in the LAN party is dropped in Part 2.
    longest_password = ""
    lan_parties = nx.find_cliques(G) # nx returns clique as list of node names
    for party in lan_parties:
        password = ','.join(sorted(party))
        if len(password) > len(longest_password):
            longest_password = password
    return longest_password

if __name__ == '__main__':
    input = get_data(day=23, year=2024)
    G, part1_solution = part1(input)
    print(f"Part 1 solution: {part1_solution}")
    part2_solution = part2(G)
    print(f"Part 2 solution: {part2_solution}")


