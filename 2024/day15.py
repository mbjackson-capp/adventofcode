from aocd import get_data
import numpy as np
import re
from utils import gridify

np.set_printoptions(linewidth=1000)


input = get_data(day=15, year=2024)

example = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

example2 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""


def parse_input(data, part=1):
    arr, steps = data.split("\n\n")
    if part == 2:
        arr = re.sub("#", "##", arr)
        arr = re.sub("O", "[]", arr)
        arr = re.sub("\.", "..", arr)
        arr = re.sub("\@", "@.", arr)
    arr = gridify(arr)
    steps = [char for char in steps if char != "\n"]

    walls = set()
    boxes = set()
    floor = set()
    if part == 2:
        wide_boxes = set()
    for x, row in enumerate(arr):
        for y, cell_val in enumerate(row):
            if cell_val == "@":
                robot = (x, y)
            elif cell_val == "O":
                boxes.add((x, y))
            elif part == 2 and cell_val == "[" and row[y + 1] == "]":
                wide_boxes.add(((x, y), (x, y + 1)))
            elif cell_val == "#":
                walls.add((x, y))
            elif cell_val == ".":
                floor.add((x, y))
    warehouse = {"robot": robot, "walls": walls, "boxes": boxes, "floor": floor}
    if part == 2:
        warehouse["wide_boxes"] = wide_boxes

    return warehouse, steps


def map_out(warehouse: dict):
    # Assumes outer edges are all wall in all possible inputs
    x_max = max([i[0] for i in warehouse["walls"]]) + 1
    y_max = max(i[1] for i in warehouse["walls"]) + 1
    to_print = []
    for x in range(x_max):
        new_row = []
        for y in range(y_max):
            if (x, y) in warehouse["walls"]:
                new_row.append("#")
            elif (x, y) in warehouse["boxes"]:
                new_row.append("O")
            elif (x, y) == warehouse["robot"]:
                new_row.append("@")
            elif "wide_boxes" in warehouse.keys() and (x, y) in [
                i[0] for i in warehouse["wide_boxes"]
            ]:
                new_row.append("[")
            elif "wide_boxes" in warehouse.keys() and (x, y) in [
                i[1] for i in warehouse["wide_boxes"]
            ]:
                new_row.append("]")
            else:
                new_row.append(".")
        to_print.append(new_row)
    return np.array(to_print)


def spot_ahead_of(start: tuple[int, int], dir: str) -> tuple[int, int]:
    x, y = start
    if dir == "^":
        return (x - 1, y)
    elif dir == ">":
        return (x, y + 1)
    elif dir == "v":
        return (x + 1, y)
    elif dir == "<":
        return (x, y - 1)
    else:
        raise ValueError("Direction not '^', '>', 'v', or '<' ")


def do_one_step(wh: dict, step: str) -> dict:
    spot_ahead = spot_ahead_of(wh["robot"], step)
    if spot_ahead in wh["walls"]:
        return wh  # do nothing if robot would go into a wall
    elif spot_ahead_of(wh["robot"], step) in wh["boxes"]:
        boxes_ahead = [spot_ahead]
        further_spot_ahead = spot_ahead_of(spot_ahead, step)
        while True:
            if further_spot_ahead in wh["boxes"]:
                boxes_ahead.append(further_spot_ahead)
                further_spot_ahead = spot_ahead_of(further_spot_ahead, step)
            elif further_spot_ahead in wh["walls"]:
                return wh  # these boxes can't be pushed ahead
            else:
                break
        wh["boxes"].remove(spot_ahead)
        wh["boxes"].add(further_spot_ahead)
        wh["robot"] = spot_ahead
        return wh
    else:  # robot can pass forward without incident
        wh["robot"] = spot_ahead_of(wh["robot"], step)
        return wh


"""
HOW TO CHANGE BOX PUSHING LOGIC FOR PART 2
Robot on left or right of box: Logic stays basically the same, as you can only
push boxes in a straight line or not at all. Keep checking if the next spot ahead
is part of a valid wide box. Then, if you reach a wall, do nothing. Otherwise,
delete ALL wide boxes you found, and add new boxes where both points within the box
have spot_ahead_of() applied to them. And move robot ahead 1.

Robot up or down from box: Logic changes, since each box can have up to two boxes
ahead of it -- they could diverge in a V pattern or come back together etc.
Advance in a BFS-like manner to determine what to do, adding new boxes to queue
when detected.
while queue is not empty:
    - pop wide box from queue
    - Look at two spots directly ahead of this wide box. 
    - If either spot is a wall:
        - break, return warehouse as-is -- finding any wall means none of the boxes
        back to the original can be pushed forward
    - If both spots are field:
        - add this box to boxes_to_push_ahead, continue
    - If spot ahead left is ']', add it and spot to left of that to queue as new wide box
    - If spot ahead right is '[', add it and spot to right of that to queue as new wide box
    - If spots ahead are '[]', add them to queue as new wide box
delete ALL boxes in boxes_to_push_ahead from warehouse['wide_boxes']
add NEW boxes that each have both points shifted up to warehouse['wide_boxes']
move robot ahead one
return warehouse
you could keep box_lefts and box_rights as separate objects if you want
"""


def part1(data):
    wh, steps = parse_input(data)
    for _, step in enumerate(steps):
        wh = do_one_step(wh, step)
    gps_coordinates = [100 * box[0] + box[1] for box in wh["boxes"]]
    return sum(gps_coordinates)


if __name__ == "__main__":
    part1_solution = part1(input)
    print(f"Part 1 solution: {part1_solution}")

    wh2, steps2 = parse_input(example, part=2)
    print(map_out(wh2))
    print(wh2["wide_boxes"])
    # TODO: part2_solution = part2(input)
