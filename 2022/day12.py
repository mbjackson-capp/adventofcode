from aocd import get_data
# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np
import heapq # priority queue implementation that pops lowest priority score
import time

# Problem statement: https://adventofcode.com/2022/day/12


input = get_data(day=12, year=2022).split('\n')
peak = np.array([[char for char in str] for str in input], dtype=str)

def start_and_end(map):
    start = tuple(np.argwhere(map == 'S')[0])
    end = tuple(np.argwhere(map == 'E')[0])
    return start, end

def elev(char):
    '''Get a numerical representation of elevation for comparisons'''
    ORD_A = 97
    if char == 'S':
        return 0
    elif char == 'E':
        return 26
    else:
        return ord(char) - ORD_A

def passable(peak, curr_node, neighbor):
    '''Determines whether it's possible for the climber to advance from their
    current spot to the neighboring spot.'''
    curr_x, curr_y = curr_node
    neigh_x, neigh_y = neighbor
    return (elev(peak[neigh_x, neigh_y]) - elev(peak[curr_x, curr_y]) <= 1)

def neighbor_locs(array, x, y, include_diag=False):
    '''Returns the indices of neighbors of a location in a square array.
    Reused with modifications from my 2021 Day 11.'''
    max_x, max_y = array.shape
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
                    and this_x < max_x and this_y < max_y):
                    neighbor_locs.append((this_x, this_y))
    return neighbor_locs

def dijkstra_climb(peak, start_node=(0,0), end_node='default', part=1):
    '''
    Use Dijkstra's algorithm to find a shortest path up a map where letters
    represent elevations. If adjacent spot is at most one letter later than
    current spot, it can be added to path; if not, it can't.
    Priority queue implementation inspired by
    https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/.
    Comments on steps adapted from Wikipedia, "Dijkstra's algorithm"
    '''
    max_x, max_y = peak.shape
    if end_node == 'default':
        end_node = (max_x-1, max_y-1)
    # unattainably high value, since np.inf isn't usable in int-dtype array
    INF = max_y * max_x + 1

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
        
        #Ignore points that cannot be passed into
        neighbors = [pt for pt in neighbor_locs(peak, curr_x, curr_y) 
                     if passable(peak, curr_node, pt)]
        for neighbor in neighbors:
            neigh_dist = curr_dist + 1
            # Compare newly calculated tentative distance to the earlier value
            # and keep the smaller of the two
            if neigh_dist < distances[neighbor]:
                distances[neighbor] = neigh_dist
                # keep track of unvisited nodes with finite tentative distance
                heapq.heappush(priority_queue, (neigh_dist, neighbor))

    return distances[end_node]


if __name__ == '__main__':
    start, end = start_and_end(peak)
    print(f"Part 1 answer: {dijkstra_climb(peak, start_node=start, end_node=end)}")

    P2_INF = 9999999
    p2_ans = P2_INF
    for poss_start in np.argwhere(peak=='a'):
        start = tuple(poss_start)
        path_length = dijkstra_climb(peak, start_node=start, end_node=end)
        if path_length < p2_ans:
            p2_ans = path_length
    print(f"Part 2 answer: {p2_ans}") #Takes about 3 seconds
