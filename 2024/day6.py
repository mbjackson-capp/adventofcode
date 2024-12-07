from aocd import get_data
from copy import deepcopy
import numpy as np

input = np.array(
    [[char for char in row] for row in get_data(day=6, year=2024).split("\n")]
)


def find_guard(arr: np.ndarray):
    # without type conversion you get, e.g. (array([6]), array([4]))
    return [int(i[0]) for i in np.where(arr == "^")]


def next(x, y, header):
    """Return next spot that guard will walk to if moving straight ahead"""
    if header == "^":
        x -= 1
    elif header == ">":
        y += 1
    elif header == "v":
        x += 1
    elif header == "<":
        y -= 1
    return x, y


class Guard:
    def __init__(self, x, y, header="^"):
        self.x = x
        self.y = y
        self.header = header
        self.visited = [(self.x, self.y)]

    def turn(self):
        HEADERS = "^>v<"
        header_ix = HEADERS.index(self.header)
        new_ix = (header_ix + 1) % len(HEADERS)
        self.header = HEADERS[new_ix]

    def in_front_of(self, arr):
        front_x, front_y = next(self.x, self.y, self.header)
        try:
            return arr[front_x][front_y]
        except IndexError:
            return None

    def move(self, arr):
        arr[self.x][self.y] = "X"
        if self.in_front_of(arr) in ["#", "O"]:
            self.turn()
        else:
            self.x, self.y = next(self.x, self.y, self.header)
            self.visited.append((self.x, self.y))

    def is_on_map(self, arr):
        return (0 <= self.x < len(arr)) and (0 <= self.y < len(arr[0]))

    def has_cycled(self):
        """Determine if current spot AND spot ahead occur right after the
        other on the already-visited list. This can only happen if the path has cycled
        """
        if (self.x, self.y) in self.visited:
            spot_ix = self.visited.index((self.x, self.y))
            try:
                if self.visited[spot_ix + 1] == next(self.x, self.y, self.header):
                    return True
            except IndexError:
                return False
        return False


def patrol(arr: np.array, get_path=False):
    start_x, start_y = find_guard(arr)
    g = Guard(start_x, start_y)
    while g.is_on_map(arr):
        if g.has_cycled():
            break
        g.move(arr)
    if get_path:
        return g.visited[:-1], g.has_cycled()
    else:
        return (arr == "X").sum(), g.has_cycled()


def count_obstacle_spots(arr: np.array, verbose=True) -> int:
    """Count the number of spots on the map at which it's possible to place an obstacle
    and cause the guard to become trapped in a cycle. To save time, looks only at spots
    that the guard could have walked across in the original map.
    This still takes several (between 20 and 60) minutes to run on the 130x130 input."""
    count = 0
    possible_spots, _ = patrol(deepcopy(arr), get_path=True)
    # For ease of tracking progress, check possible spots in grid order
    possible_spots = sorted(list(set(possible_spots)), key=lambda x: (x[0], x[1]))
    for spot in possible_spots:
        x, y = spot
        new_arr = deepcopy(arr)
        if new_arr[x][y] == ".":
            new_arr[x][y] = "O"
            _, this_arr_cycled = patrol(new_arr)
            if this_arr_cycled and verbose:
                print(f"Cycle detected with obstacle at {x,y}!")
            count += this_arr_cycled
    return count


if __name__ == "__main__":
    print(f"Now running Part 1. This may take a second...")
    part1_solution, _ = patrol(deepcopy(input))

    print(f"Now running Part 2. This will take several minutes...")
    part2_solution = count_obstacle_spots(deepcopy(input), verbose=True)

    print(f"\nPart 1 solution: {part1_solution}")
    print(f"Part 2 solution: {part2_solution}")
