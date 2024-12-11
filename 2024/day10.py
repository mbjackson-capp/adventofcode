from aocd import get_data
import numpy as np



def gridify(mapstr: str) -> np.array:
    """TODO: Put this in a utils file"""
    return np.array([[int(char) for char in row] for row in mapstr.split('\n')])

def get_trail_starts(arr: np.array):
    where_x, where_y = np.where(arr == 0)
    return zip([int(x) for x in where_x], [int(y) for y in where_y])

def neighbor_locs(arr, x, y, include_diag=False):
    """Returns the indices of neighbors of a location in a square array.
    TODO: Put this in a utils file"""
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
                if (
                    this_x >= 0
                    and this_y >= 0
                    and this_x < len(arr)
                    and this_y < len(arr[0])
                ):
                    neighbor_locs.append((this_x, this_y))
    return neighbor_locs 

def get_trails_starting_at(arr: np.ndarray, x, y, prior_step_val=-1):
    """Obtain all valid trails, i.e. paths that are never diagonal,
    start at 0, and increment by 1 at each step until they terminate
    at 9."""
    if prior_step_val < 0 and arr[x][y] != 0:
        raise Exception("Trail should not start here!") 
    elif arr[x][y] == 9 and prior_step_val == 8: #Base case: Trail over
        return [[(x,y)]]
    elif arr[x][y] == prior_step_val + 1:
        neighbors = neighbor_locs(arr, x, y)
        results = []
        for nbr in neighbors:
            x_n, y_n = nbr
            if arr[x_n][y_n] == arr[x][y] + 1:
                trails = get_trails_starting_at(arr, x_n, y_n, prior_step_val=arr[x][y])
                for trail in trails:
                    trail.insert(0, (x,y))
                    results.append(trail)
        return results


def run(arr):
    p1_scores = []
    p2_scores = []
    all_trails = []
    starts = get_trail_starts(arr)
    for start in starts:
        ends = set()
        start_x, start_y = start
        trails_from_here = get_trails_starting_at(arr, start_x, start_y)
        p2_scores.append(len(trails_from_here))
        for trail in trails_from_here:
            if trail[-1] not in ends:
                ends.add(trail[-1])
                all_trails.append(trail)
        p1_scores.append(len(ends))
    return sum(p1_scores), sum(p2_scores), all_trails


if __name__ == '__main__':
    input = gridify(get_data(day=10, year=2024))
    total_p1_score, total_p2_score, trails = run(input)
    print(f"Part 1 solution: {total_p1_score}")
    print(f"Part 2 solution: {total_p2_score}")