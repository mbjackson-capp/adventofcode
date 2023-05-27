from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import numpy as np

#Problem statement: https://adventofcode.com/2021/day/9

input = get_data(day=9, year=2021).split('\n')

seafloor = np.array([[int(char) for char in str] for str in input], dtype=int)

def neighbor_locs(seafloor, x, y):
    '''Returns the indices of neighbor points that exist on the seafloor'''
    neighbor_locs = []
    for tuple in ((x, y+1), (x+1, y), (x, y-1), (x-1, y)):
        neighbor_x, neighbor_y = tuple
        if (neighbor_x >= 0 and neighbor_y >= 0 
            and neighbor_x < len(seafloor) and neighbor_y < len(seafloor)):
            neighbor_locs.append(tuple)
    return neighbor_locs

def neighbors(seafloor, x, y):
    '''Returns the values at neighbor points that exist on the seafloor'''
    neighbors = []
    for tuple in neighbor_locs(seafloor, x, y):
        neighbor_x, neighbor_y = tuple
        neighbors.append(seafloor[neighbor_x][neighbor_y])
    return neighbors

def get_low_points(seafloor):
    low_points = []
    for x in range(len(seafloor)):
        for y in range(len(seafloor)):
            if seafloor[x][y] < min(neighbors(seafloor, x, y)):
                low_points.append((x, y))
    return low_points

def part1(seafloor):
    risk_score = 0
    low_points = get_low_points(seafloor)
    for point in low_points:
        x, y = point
        risk_score += 1 + seafloor[x][y]
    return risk_score

def basin_size(point, seafloor):
    '''Basic recursive flood fill algorithm, using -1 to indicate filled.
    Input point is a (x, y) tuple for current coordinate on seafloor'''
    curr_x, curr_y = point
    if seafloor[curr_x][curr_y] in (9, -1):
        return 0
    else:
        seafloor[curr_x][curr_y] = -1 
        return 1 + sum([basin_size(pt, seafloor) for pt in 
                        neighbor_locs(seafloor, curr_x, curr_y)])

def part2(seafloor):
    low_points = get_low_points(seafloor)
    basin_sizes = [basin_size(point, seafloor) for point in low_points]
    basin_sizes.sort(reverse=True)
    return np.product(basin_sizes[0:3])


if __name__ == '__main__':
    print(f"Part 1 answer: {part1(seafloor)}")
    print(f"Part 2 answer: {part2(seafloor)}")
