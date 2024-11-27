from aocd import get_data
from computer import Computer

input = [int(i) for i in get_data(day=11, year=2019).split(",")]

c = Computer(intcode=input)

DIRS = "NESW"
BLACK = 0
WHITE = 1


class Robot:
    def __init__(self, part=1):
        self.x = 0
        self.y = 0
        self.heading = "N"
        self.hull_map = {(0, 0): BLACK} if part == 1 else {(0, 0): WHITE}
        self.ever_painted = set()

    def check_camera(self):
        if (self.x, self.y) not in self.hull_map:
            self.hull_map[(self.x, self.y)] = BLACK
        return self.hull_map[(self.x, self.y)]

    def paint_panel(self, paint_output: int):
        if paint_output == 0:
            self.hull_map[(self.x, self.y)] = BLACK
        elif paint_output == 1:
            self.hull_map[(self.x, self.y)] = WHITE
        else:
            raise ValueError(
                f"Paint instruction should be 0 or 1, but got: {paint_output}"
            )
        self.ever_painted.add((self.x, self.y))

    def turn(self, dir_output: int):
        """
        Turn the robot right or left in response to intcode computer output.
        """
        if dir_output == 0:  # turn left
            self.heading = DIRS[(DIRS.index(self.heading) - 1) % 4]
        elif dir_output == 1:  # turn right
            self.heading = DIRS[(DIRS.index(self.heading) + 1) % 4]
        else:
            raise ValueError(
                f"Turn instruction should be 0 or 1, but got: {dir_output}"
            )

    def move(self):
        """Move robot one step ahead in direction of heading"""
        if self.heading == "N":
            self.y += 1
        elif self.heading == "S":
            self.y -= 1
        elif self.heading == "E":
            self.x += 1
        elif self.heading == "W":
            self.x -= 1


def solve(part=1):
    c = Computer(intcode=input)
    r = Robot(part=part)
    while c.status != "halted":
        curr_color = r.check_camera()
        if curr_color == BLACK:
            input_val = 0
        elif curr_color == WHITE:
            input_val = 1
        paint_output = c.process(initial_inputs=[input_val], pause_at_output=True)
        dir_output = c.process(pause_at_output=True)
        r.paint_panel(paint_output)
        r.turn(dir_output)
        r.move()
    if part == 1:
        return len(r.ever_painted)
    elif part == 2:
        return draw_map(r.hull_map)


def draw_map(hull_map: dict) -> list[list[int]]:
    min_x = min([i[0] for i in hull_map.keys()])
    min_y = min([i[1] for i in hull_map.keys()])
    # rescale so all indices are nonnegative and start at 0
    map_fixed = {(k[0] - min_x, k[1] - min_y): v for k, v in hull_map.items()}
    # create array of proper dimensions
    len_x = max(i[0] for i in map_fixed.keys()) + 1
    len_y = max(i[1] for i in map_fixed.keys()) + 1
    arr = [[0 for i in range(len_x)] for j in range(len_y)]
    for k, v in map_fixed.items():
        x, y = k
        if v == 1:
            arr[y][x] = 1
    return arr  # beware: letters get transcribed upside-down!


if __name__ == "__main__":
    part1 = solve(part=1)
    part2 = solve(part=2)
    print(f"Part 1 solution: {part1}")
    print(f"Part 2 solution (highlight '1' to see letters more clearly:)")
    for row in part2[::-1]:  # fix upside-down transcription
        print(row)
