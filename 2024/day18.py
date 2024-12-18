from aocd import get_data
import numpy as np
from math import inf
import heapq
from utils import neighbor_locs


def listify_bytes(bytes):
    result = []
    listified = [row.split(",") for row in bytes.split("\n")]
    for thing in listified:
        tuple = (int(thing[0]), int(thing[1]))
        result.append(tuple)
    return result


def bytefall(grid: np.array, bytes, up_to=None):
    if type(bytes) != list:
        bytes = listify_bytes(bytes)
    for ix, byte in enumerate(bytes):
        if up_to is not None and ix >= up_to:
            break
        grid[byte] = "#"
    return grid


def dijkstra(arr, start_node=(0, 0), end_node="default"):
    max_y, max_x = arr.shape
    if end_node == "default":
        end_node = (max_x - 1, max_y - 1)

    distances = {}
    for x in range(max_x):
        for y in range(max_y):
            node = (x, y)
            distances[node] = 0 if node == start_node else inf

    priority_queue = [(0, start_node)]

    while len(priority_queue) > 0:
        curr_dist, curr_node = heapq.heappop(priority_queue)
        curr_x, curr_y = curr_node
        neighbors = [pt for pt in neighbor_locs(arr, curr_x, curr_y) if arr[pt] != "#"]
        for neighbor in neighbors:
            neigh_dist = curr_dist + 1
            if neigh_dist < distances[neighbor]:
                distances[neighbor] = neigh_dist
                heapq.heappush(priority_queue, (neigh_dist, neighbor))

    return distances[end_node]


if __name__ == "__main__":
    MEMORY_SPACE_SIZE = 71
    grid = np.full((MEMORY_SPACE_SIZE, MEMORY_SPACE_SIZE), ".")
    FIRST_KILOBYTE = 1024
    input = get_data(day=18, year=2024)
    grid = bytefall(grid, input, up_to=FIRST_KILOBYTE)

    part1 = dijkstra(grid)
    remaining_bytes = listify_bytes(input)[FIRST_KILOBYTE:]

    while True:
        grid = bytefall(grid, remaining_bytes, up_to=1)
        latest_coords = remaining_bytes.pop(0)
        print(f"Byte fell at {latest_coords}")
        path_len = dijkstra(grid)
        print(f"New shortest path length: {path_len}")
        if path_len == inf:
            break

    print(f"Part 1 solution: {part1}")
    print(f"Part 2 solution: {latest_coords}")
