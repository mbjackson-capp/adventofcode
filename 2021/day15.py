from aocd import get_data
# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import heapq # priority queue implementation that pops lowest priority score

# Problem statement: https://adventofcode.com/2021/day/15

input = get_data(day=15, year=2021).split('\n')
cavern = np.array([[int(char) for char in str] for str in input], dtype=int)

def neighbor_locs(sqarray, x, y, include_diag=False):
    '''Returns the indices of neighbors of a location in a square array.
    Reused with modifications from my 2021 Day 11.'''
    neighbor_locs = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            if not include_diag and dx != 0 and dy != 0:
                continue
            else:
                this_x = x + dx
                this_y = y + dy
                if (this_x >= 0 and this_y >= 0
                    and this_x < len(sqarray) and this_y < len(sqarray)):
                    neighbor_locs.append((this_x, this_y))
    return neighbor_locs

def neighbor_vals(sqarray, x, y):
    '''Returns the values at neighbor points to a given index of a square array.
    Reused with modifications from my 2021 Day 9.'''
    neighbors = []
    for tuple in neighbor_locs(sqarray, x, y):
        neighbor_x, neighbor_y = tuple
        neighbors.append(sqarray[neighbor_x][neighbor_y])
    return neighbors

def expand(cavern):
    '''Create the expanded-size map for Part 2'''
    expanded = np.concatenate([cavern + i for i in range(5)], axis=1)
    expanded = np.concatenate([expanded + i for i in range(5)], axis=0)
    expanded[expanded > 9] -= 9
    return expanded
    

def dijkstra_pq(cavern, start_node=(0,0), end_node='default', part=1):
    '''
    Priority queue implementation inspired by
    https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/.
    Comments on steps adapted from Wikipedia, "Dijkstra's algorithm"
    '''
    if part == 2:
        cavern = expand(cavern)
    max_y, max_x = cavern.shape
    if end_node == 'default':
        end_node = (max_x-1, max_y-1)
    # unattainably high value, since np.inf isn't usable in int-dtype array
    INF = np.sum(cavern) + 1

    # Assign to every node a tentative distance value
    distances = {}
    for x in range(max_x):
        for y in range(max_y):
            node = (x, y)
            distances[node] = 0 if node == start_node else INF

    priority_queue = [(0, start_node)]

    while len(priority_queue) > 0:
        # Select the unvisited node that is marked with the smallest tentative
        # distance; set it as the new current node to "visit" it
        curr_dist, curr_node = heapq.heappop(priority_queue)

        # Calculate tentative distances to each unvisited neighbor through 
        # current node
        curr_x, curr_y = curr_node
        neighbors = [pt for pt in neighbor_locs(cavern, curr_x, curr_y)]
        # for just unvisited neighbors, add "if not pt in [i[1] for i in priority_queue]" 
        # to above comprehension. But that's unnecessary and slows performance
        for neighbor in neighbors:
            neigh_x, neigh_y = neighbor
            neigh_dist = curr_dist + cavern[neigh_x][neigh_y]
            # Compare newly calculated tentative distance to the earlier value
            # and keep the smaller of the two
            if neigh_dist < distances[neighbor]:
                distances[neighbor] = neigh_dist
                # keep track of unvisited nodes with finite tentative distance
                heapq.heappush(priority_queue, (neigh_dist, neighbor))

    return distances[end_node]


if __name__ == '__main__':
    print(f"Part 1 answer: {dijkstra_pq(cavern)}")
    print(f"Part 2 answer: {dijkstra_pq(cavern, part=2)}")   

