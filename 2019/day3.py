from aocd import get_data

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2019/day/3

input = get_data(day=3, year=2019).split("\n")
wire0, wire1 = [wire.split(",") for wire in input]

wire0_points = set()
wire1_points = set()

central_port = (0, 0)
curr_loc = [0, 0]


def reset():
    """
    Put the current location of the tracker back at the central port.
    You could probably make new trackers as objects come to think of it.
    """
    global curr_loc
    curr_loc = [0, 0]


def read_segment(segment, target_set):
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
    global curr_loc

    # print(segment)
    dir = segment[0]
    dist = int(segment[1:])
    for i in range(dist):
        if dir == "R":
            curr_loc[0] += 1
        elif dir == "L":
            curr_loc[0] -= 1
        elif dir == "U":
            curr_loc[1] += 1
        elif dir == "D":
            curr_loc[1] -= 1
        # print(curr_loc)
        target_set.add(tuple(curr_loc))


for segment in wire0:
    read_segment(segment, wire0_points)
reset()
for segment in wire1:
    read_segment(segment, wire1_points)

intersections = wire0_points.intersection(wire1_points)
# print(intersections)


def manhattan_dist(p1, p2):
    """
    Returns the Manhattan distance between two points in the xy plane.

    Inputs:
        -point1, point2 (tuple): tuples of length 2, each entry in each tuple
        is an int; representing points (x, y)
    Returns (int): Manhattan distance
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


manhattans = [manhattan_dist(point, (0, 0)) for point in list(intersections)]
print(min(manhattans))

# you calculated list of intersections already. No need to recalculate it


def intersection_distances(wire, intersections):
    """
    Takes in a wire (list of segments like "U330") and traverses it point by
    point. If at any point it reaches a known intersection, note the intersection
    adn
    into a set of points. Then adds those points to a set (consisting of all
    points previously recorded on the wire).

    Inputs:
        -segment(str): an instruction such as "U330" or "D57", which denotes
        the direction in which the wire goes and how far it's going in that
        direction
        -target_set(set): a set of points that will be written to.
    Returns: None, modifies target_set in place
    """
    global curr_loc

    total_traversed = 0
    inter_dict = {}

    # print(segment)
    for segment in wire:
        dir = segment[0]
        dist = int(segment[1:])
        for i in range(dist):
            if dir == "R":
                curr_loc[0] += 1
            elif dir == "L":
                curr_loc[0] -= 1
            elif dir == "U":
                curr_loc[1] += 1
            elif dir == "D":
                curr_loc[1] -= 1
            # print(curr_loc)
            total_traversed += 1
            if tuple(curr_loc) in intersections:
                inter_dict[tuple(curr_loc)] = total_traversed

    return inter_dict


reset()
distances0 = intersection_distances(wire0, intersections)
reset()
distances1 = intersection_distances(wire1, intersections)

joint_distances = []
for point, dist in distances0.items():
    if point in distances1:
        joint_distances.append(dist + distances1[point])
print(min(joint_distances))
