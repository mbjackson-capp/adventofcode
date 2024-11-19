from aocd import get_data

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2019/day/3

input = get_data(day=3, year=2019).split("\n")


class Tracker:
    def __init__(self):
        self.x = 0
        self.y = 0

    def reset(self):
        self.x = 0
        self.y = 0


def read_segment(segment, target_set, t: Tracker):
    """
    Takes in a description of a segment of wire (e.g. "U330") and converts it
    into a set of points. Then adds those points to a set (consisting of all
    points previously recorded on the wire).

    Inputs:
        -segment(str): an instruction such as "U330" or "D57", which denotes
        the direction in which the wire goes and how far it's going in that
        direction
        -target_set(set): a set of points that will be written to.
    Returns: None, modifies target_set in place
    """

    dir = segment[0]
    dist = int(segment[1:])
    for _ in range(dist):
        if dir == "R":
            t.x += 1
        elif dir == "L":
            t.x -= 1
        elif dir == "U":
            t.y += 1
        elif dir == "D":
            t.y -= 1
        target_set.add((t.x, t.y))


def manhattan_dist(p1, p2):
    """
    Returns the Manhattan distance between two points in the xy plane.

    Inputs:
        -point1, point2 (tuple): tuples of length 2, each entry in each tuple
        is an int; representing points (x, y)
    Returns (int): Manhattan distance
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def intersection_distances(wire, intersections, t: Tracker):
    """
    Helper function for part 2. Assumes that list of intersections was already
    calculated when solving part 1. no need to recalculate it.
    """

    total_traversed = 0
    inter_dict = {}

    for segment in wire:
        dir = segment[0]
        dist = int(segment[1:])
        for _ in range(dist):
            if dir == "R":
                t.x += 1
            elif dir == "L":
                t.x -= 1
            elif dir == "U":
                t.y += 1
            elif dir == "D":
                t.y -= 1
            total_traversed += 1
            if (t.x, t.y) in intersections:
                inter_dict[(t.x, t.y)] = total_traversed

    return inter_dict


def main():
    wire0, wire1 = [wire.split(",") for wire in input]
    wire0_points = set()
    wire1_points = set()

    t = Tracker()
    for segment in wire0:
        read_segment(segment, wire0_points, t)
    t.reset()
    for segment in wire1:
        read_segment(segment, wire1_points, t)

    intersections = wire0_points.intersection(wire1_points)
    manhattans = [manhattan_dist(point, (0, 0)) for point in list(intersections)]
    print(f"Part 1 solution: {min(manhattans)}")

    t.reset()
    distances0 = intersection_distances(wire0, intersections, t)
    t.reset()
    distances1 = intersection_distances(wire1, intersections, t)

    joint_distances = []
    for point, dist in distances0.items():
        if point in distances1:
            joint_distances.append(dist + distances1[point])
    print(f"Part 2 solution: {min(joint_distances)}")


if __name__ == "__main__":
    main()
