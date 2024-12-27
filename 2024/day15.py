from aocd import get_data
import numpy as np
import re
from utils import gridify

np.set_printoptions(linewidth=1000)


def parse_input(data: str, part: int=1) -> dict:
    """Turn input into its constituent warehouse (representing each
    set of relevant components as a key-value pair in a dict) and its
    string of step instructions."""
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
    box_lefts = set()
    box_rights = set()
    for x, row in enumerate(arr):
        for y, cell_val in enumerate(row):
            if cell_val == "@":
                robot = (x, y)
            elif cell_val == "O":
                boxes.add((x, y))
            elif part == 2 and cell_val == "[" and row[y + 1] == "]":
                box_lefts.add((x,y))
                box_rights.add((x, y+1))
            elif cell_val == "#":
                walls.add((x, y))

    warehouse = {
        "robot": robot, 
        "walls": walls, 
        "boxes": boxes,
        "box_lefts": box_lefts,
        "box_rights": box_rights
        }

    return warehouse, steps


def map_out(warehouse: dict) -> np.array:
    """Returns a graphical representation of the warehouse dictionary, as shown 
    in problem statement. For debugging purposes only."""
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
            elif "box_lefts" in warehouse.keys() and (x, y) in warehouse["box_lefts"]:
                new_row.append("[")
            elif "box_rights" in warehouse.keys() and (x, y) in warehouse["box_rights"]: 
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
    # Do-nothing case: Robot up against wall
    if spot_ahead in wh["walls"]:
        return wh  
    
    # PART 1 BOX-PUSHING LOGIC
    elif spot_ahead in wh["boxes"]:
        boxes_ahead = [spot_ahead]
        further_spot_ahead = spot_ahead_of(spot_ahead, step)
        while True:
            if further_spot_ahead in wh["boxes"]:
                boxes_ahead.append(further_spot_ahead)
                further_spot_ahead = spot_ahead_of(further_spot_ahead, step)
            elif further_spot_ahead in wh["walls"]: # these boxes can't be pushed ahead
                return wh  
            else:
                break
        wh["boxes"].remove(spot_ahead)
        wh["boxes"].add(further_spot_ahead)
        wh["robot"] = spot_ahead
        return wh
    
    # PART 2 BOX-PUSHING LOGIC
    elif (spot_ahead in wh["box_rights"] or spot_ahead in wh["box_lefts"]):
        box_rights_ahead = [spot_ahead] if spot_ahead in wh['box_rights'] else []
        box_lefts_ahead = [spot_ahead] if spot_ahead in wh['box_lefts'] else []

        # 2a. PUSH BOXES LEFT OR RIGHT
        # Still linear; add alternating box_right and box_left elements in front of 
        # this point until you hit a wall (in which case return immediately) or
        # until you hit empty space
        if step in ('<', '>'):  
            further_spot_ahead = spot_ahead_of(spot_ahead, step)
            while True:
                if further_spot_ahead in wh['box_rights']:
                    box_rights_ahead.append(further_spot_ahead)
                    further_spot_ahead = spot_ahead_of(further_spot_ahead, step)
                elif further_spot_ahead in wh['box_lefts']:
                    box_lefts_ahead.append(further_spot_ahead)
                    further_spot_ahead = spot_ahead_of(further_spot_ahead, step)
                elif further_spot_ahead in wh['walls']: # these boxes can't be pushed ahead
                    return wh
                else:
                    break 

        # 2b. PUSH BOXES UP OR DOWN
        # Each box can have up to two boxes ahead of it -- they could branch out
        # into V-shaped or tree-like patterns, converge back together, etc.
        # If there is ANY wall in front of ANY box ahead, NONE of them get pushed.
        # Advance in a BFS-like manner with a queue to detect new boxes in front of
        # already-detected ones, until you hit a wall in front of any box or see
        # empty floor in front of every box.
        elif step in ('^', 'v'):
            # add the other half of the first box
            if box_rights_ahead:
                other_half = spot_ahead_of(spot_ahead, '<')
                box_lefts_ahead.append(other_half)
            elif box_lefts_ahead:
                other_half = spot_ahead_of(spot_ahead, '>')
                box_rights_ahead.append(other_half)

            q = [spot_ahead_of(spot_ahead, step), spot_ahead_of(other_half, step)]
            while len(q) > 0:
                further_spot_ahead = q.pop(0)

                if further_spot_ahead in wh['walls']:
                    return wh
                
                elif further_spot_ahead in wh['box_rights']:
                    other_half = spot_ahead_of(further_spot_ahead, '<')
                    box_rights_ahead.append(further_spot_ahead)
                    box_lefts_ahead.append(other_half)
                    q.append(spot_ahead_of(further_spot_ahead, step))
                    q.append(spot_ahead_of(other_half, step))  

                elif further_spot_ahead in wh['box_lefts']:
                    other_half = spot_ahead_of(further_spot_ahead, '>')
                    box_lefts_ahead.append(further_spot_ahead)
                    box_rights_ahead.append(other_half)
                    q.append(spot_ahead_of(further_spot_ahead, step))
                    q.append(spot_ahead_of(other_half, step))

                else: # There is unoccupied floor ahead of this box segment. Good!
                    continue 

        # Push all spotted box segments ahead by one and move robot ahead
        box_rights_to_add = [spot_ahead_of(br, step) for br in box_rights_ahead]
        box_lefts_to_add = [spot_ahead_of(bl, step) for bl in box_lefts_ahead]
        wh['box_rights'] = (wh['box_rights'] - set(box_rights_ahead)) | set(box_rights_to_add)
        wh['box_lefts'] = (wh['box_lefts'] - set(box_lefts_ahead)) | set(box_lefts_to_add)
        wh['robot'] = spot_ahead
        return wh
    
    # Move-without-incident case: Robot can pass forward on floor
    else:  
        wh["robot"] = spot_ahead
        return wh


def run(data, part=1, debug=False):
    wh, steps = parse_input(data, part=part)
    if debug:
        print(f"Initial state:")
        print(map_out(wh))
    for _, step in enumerate(steps):
        if debug:
            print(f"Move {step}:")
        wh = do_one_step(wh, step)
        if debug:
            print(map_out(wh))
    gps_coordinates = (
        [100 * box[0] + box[1] for box in wh["boxes"]] 
        if part == 1 
        else [100 * box[0] + box[1] for box in wh["box_lefts"]]
    )
    return sum(gps_coordinates)


if __name__ == "__main__":
    input = get_data(day=15, year=2024)
    part1_solution = run(input)
    print(f"Part 1 solution: {part1_solution}")
    part2_solution = run(input, part=2)
    print(f"Part 2 solution: {part2_solution}")
