from aocd import get_data

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=3, year=2015)


def delivery_walk(moves: str, part=1):
    santas = [[0, 0]] if part == 1 else [[0, 0], [0, 0]]
    visited = {(0, 0): 1}
    for turn, move in enumerate(moves):
        # always moves the only Santa if part == 1;
        # alternates between Santa and Robo-Santa if part == 2
        i = turn % part
        x, y = santas[i]
        if move == "^":
            y += 1
        elif move == ">":
            x += 1
        elif move == "v":
            y -= 1
        elif move == "<":
            x -= 1
        santas[i] = (x, y)
        if (x, y) not in visited:
            visited[(x, y)] = 0
        visited[(x, y)] += 1
    return len(visited.keys())


part1 = delivery_walk(input)
print(f"Part 1 solution: {part1}")
part2 = delivery_walk(input, part=2)
print(f"Part 2 solution: {part2}")
