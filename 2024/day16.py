from aocd import get_data
from enum import Enum
import heapq
from math import inf
import numpy as np
from utils import gridify, neighbor_locs


class Direction(int, Enum):
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    # Needs comparison methods in order to avoid 'TypeError' when heapq.heappop()
    # finds two entries of equal priority in the queue
    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    # Needs this method to avoid "unhashable type: Direction" if comparison methods
    # are instantiated
    def __hash__(self):
        return hash(self.value)


TURN_SCORE = 1000


def find_S_and_E(arr):
    """Find single starting spot"""
    spot_S = tuple(int(i[0]) for i in np.where(arr == "S"))
    spot_E = tuple(int(i[0]) for i in np.where(arr == "E"))
    return spot_S, spot_E


def get_dir_from(old_pt: tuple[int, int], new_pt: tuple[int, int]):
    old_x, old_y = old_pt
    if new_pt == (old_x, old_y + 1):
        return Direction.EAST
    elif new_pt == (old_x + 1, old_y):
        return Direction.SOUTH
    elif new_pt == (old_x, old_y - 1):
        return Direction.WEST
    elif new_pt == (old_x - 1, old_y):
        return Direction.NORTH


def backtrack_pt(new_pt: tuple[int, int], dir: Direction):
    """Get the point FROM which you had to come to enter new point from a given
    direction. Used in backtracking for Part 2."""
    new_x, new_y = new_pt
    if dir == Direction.EAST:
        return (new_x, new_y - 1)
    elif dir == Direction.SOUTH:
        return (new_x - 1, new_y)
    elif dir == Direction.WEST:
        return (new_x, new_y + 1)
    elif dir == Direction.NORTH:
        return (new_x + 1, new_y)


def are_90deg_apart(old_dir: Direction, new_dir: Direction) -> bool:
    """Determine if two Directions are 90 degrees apart. Since each Direction has
    a numeric value, this will be true if their unsigned difference is 1 (for
    'within-the-compass' comparisons E-S, S-W, W-N; or S-E, W-S, N-W) or 3 (for
    'loop-around-the-compass' comparisons N-E or E-N)"""
    return abs(old_dir - new_dir) in [1, 3]


def reindeer_dijkstra(
    arr: np.array, start: tuple[int, int], end: tuple[int, int]
) -> int:
    """
    Run Dijkstra's algorithm to find the length of the shortest path
    from a starting square to an ending square, with the added proviso
    that each 90 degree turn adds 1000 to the final result.
    """
    x_max = len(arr)
    y_max = len(arr[0])

    # Assign to every node/direction-of-entry tuple a tentative distance value
    distances = {}
    for x in range(x_max):
        for y in range(y_max):
            node = (x, y)
            for dir in Direction:
                distances[(node, dir)] = 0 if node == start else inf

    pq = [(0, (start, Direction.EAST))]

    while len(pq) > 0:
        # Select unvisited node that with lowest tentative distance
        curr_dist, curr_node = heapq.heappop(pq)
        curr_node, curr_dir = curr_node

        # Calculate tentative distances to each unvisited neighbor from current node
        x_curr, y_curr = curr_node
        neighbors = [
            (pt, get_dir_from(curr_node, pt))
            for pt in neighbor_locs(arr, x_curr, y_curr)
            if arr[pt] != "#"
        ]
        for neighbor in neighbors:
            nbr, new_dir = neighbor
            nbr_dist = curr_dist + 1
            if are_90deg_apart(new_dir, curr_dir):
                nbr_dist += TURN_SCORE
            # Compare newly calculated tentative distance to previous value; keep smaller of them
            if nbr_dist < distances[(nbr, new_dir)]:
                distances[(nbr, new_dir)] = nbr_dist
                # keep track of unvisited nodes with finite tentative distance
                heapq.heappush(pq, (nbr_dist, (nbr, new_dir)))

    distances = reformat_distances(distances)
    solution = min(distances[end].values())
    return solution, distances


def reformat_distances(distances: dict) -> dict:
    """Change 'long' format dictionary in which each point/direction-of-entry
    tuple is its own key, into a 'wide' format dictionary in which each point
    is a key, and the values are themselves four-key dicts mapping each direction
    to the distance of the shortest path entering that point from that direction.
    This will help with count_spots_in_shortest_paths later on."""
    new_distances = {}
    for k, v in distances.items():
        pt, dir = k
        if pt not in new_distances:
            new_distances[pt] = {}
        if dir not in new_distances[pt]:
            new_distances[pt][dir] = v
    return new_distances


def count_spots_in_shortest_paths(end, distances):
    """Count distinct spots in ALL shortest paths of the reindeer race track."""
    all_paths = {end}
    stack = []
    for dir in distances[end]:
        p1_solution = min(distances[end].values())
        if distances[end][dir] == p1_solution:
            stack.append((backtrack_pt(end, dir), p1_solution))

    while len(stack) > 0:
        cur_pt, cur_dist = stack.pop(-1)
        all_paths.add(cur_pt)
        if (
            min(distances[cur_pt].values()) == 0
            and max(distances[cur_pt].values()) == 0
        ):
            # you've reached the beginning, no more backtracking from here --
            # but keep stack going in case other paths haven't finished evaluating
            continue
        for dir in distances[cur_pt]:
            if distances[cur_pt][dir] == cur_dist - 1:  # path continues straight back
                stack.append((backtrack_pt(cur_pt, dir), cur_dist - 1))
            elif (
                distances[cur_pt][dir] == cur_dist - TURN_SCORE - 1
            ):  # path continues at a turn
                stack.append((backtrack_pt(cur_pt, dir), cur_dist - TURN_SCORE - 1))
    return len(all_paths)


def run(arr):
    start, end = find_S_and_E(arr)
    part1_solution, distances = reindeer_dijkstra(arr, start, end)
    print(f"Part 1 solution: {part1_solution}")
    part2_solution = count_spots_in_shortest_paths(end, distances)
    print(f"Part 2 solution: {part2_solution}")


if __name__ == "__main__":
    input = gridify(get_data(day=16, year=2024))
    run(input)
