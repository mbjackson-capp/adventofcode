from aocd import get_data
from math import gcd, atan2


input = [[char for char in row] for row in get_data(day=10, year=2019).split("\n")]


def get_sweep_slopes(mp, start: tuple[int, int]):
    """Get a set of slopes to sweep to detect asteroids from a given starting point."""
    slopes_swept = set()
    start_x = start[0]
    start_y = start[1]
    width_x = len(mp)
    width_y = len(mp[0])

    left_dist = -start_x
    right_dist = width_x - start_x
    up_dist = -start_y
    down_dist = width_y - start_y
    for dx in range(left_dist, right_dist):
        for dy in range(up_dist, down_dist):
            if dx == 0 and dy == 0:  # a slope of (0,0) would never terminate
                continue
            x = start_x
            y = start_y
            # normalize increment to simplest terms
            inc_x = int(dx / gcd(dx, dy))
            inc_y = int(dy / gcd(dx, dy))
            m = (inc_x, inc_y)
            if m in slopes_swept:  # This slope has already been found!
                continue
            slopes_swept.add(m)
    return slopes_swept


def detect_along_slope(
    mp, start: tuple[int, int], slope: tuple[int, int]
) -> tuple[int, int]:
    """Travel as far as necessary to find an asteroid in one specified direction,
    without going off the edge of the map."""
    start_x, start_y = start
    inc_x, inc_y = slope
    x = start_x
    y = start_y
    width_x = len(mp)
    width_y = len(mp[0])
    while (0 <= x < width_x) and (0 <= y < width_y):
        x += inc_x
        y += inc_y
        if (x < 0) or (x >= width_x) or (y < 0) or (y >= width_x):
            # Sweep hit end of map!
            break
        # Check {x, y} for asteroid
        if mp[y][x] == "#":  # Asteroid detected at (x,y)!
            return (x, y)
        else:  # Asteroid not found yet"
            continue
    return None


def detector_sweep(mp, start: tuple[int, int]):
    """Sweep all possible angles from an asteroid to detect all other asteroids around it."""
    asteroids_detected = set()
    slopes_swept = get_sweep_slopes(mp, start=start)
    for slope in slopes_swept:
        result = detect_along_slope(mp, start, slope)
        if result is not None:
            asteroids_detected.add(result)
    return list(asteroids_detected)


def solve_part1(mp):
    width_x = len(mp)
    width_y = len(mp[0])
    results = {}
    for x in range(width_x):
        for y in range(width_y):
            if mp[y][x] == ".":
                # Can't build a base at {x,y} - no asteroid to build on!")
                continue
            elif mp[y][x] == "#":
                result = len(detector_sweep(mp, (x, y)))
                results[result] = (x, y)  # save coordinates of asteroid
    return max(results.keys()), results[max(results.keys())]


GOAL = 200


def solve_part_2(mp, base: tuple[int, int], goal=GOAL, printout=False):
    """
    Do as many circular sweeps as needed to find the GOALth asteroid, then
    return the desired value based on its coordinates.

    To get the proper order for a circular sweep starting with laser upward,
    calculate the arctangent of each slope (proxy for angle wrt starting point),
    and sort so that angle decreases while x is positive and increases again
    while x is negative (to account for limited range of arctangent).

    You can debug by printing out the map, with lasered spots labeled with the
    order in which they got lasered.
    """
    base_x, base_y = base
    mp[base_y][base_x] = "B"
    base_slopes = get_sweep_slopes(mp, base)

    def atan_key(slope):
        x1, y1 = slope
        return atan2(y1, x1)

    slopes_sorted = sorted(list(base_slopes), key=atan_key)
    qdrt_ur = [slope for slope in slopes_sorted if slope[0] >= 0 and slope[1] < 0]
    qdrt_lr = [slope for slope in slopes_sorted if slope[0] >= 0 and slope[1] >= 0]
    qdrt_ll = [slope for slope in slopes_sorted if slope[0] < 0 and slope[1] >= 0]
    qdrt_ul = [slope for slope in slopes_sorted if slope[0] < 0 and slope[1] < 0]
    slopes_proper_order = qdrt_ur + qdrt_lr + qdrt_ll + qdrt_ul
    asteroid_count = 0
    while asteroid_count < goal and any(
        ["#" in row for row in mp]
    ):  # laser may need to make multiple cycles
        for slope in slopes_proper_order:
            result = detect_along_slope(mp, base, slope)
            if result is not None:
                x, y = result
                asteroid_count += 1
                mp[y][x] = str(asteroid_count)
                if asteroid_count == goal:
                    if printout:
                        for row in mp:
                            print(row)
                    return (x * 100) + y
    print(f"There were fewer than {goal} asteroids to remove! Check your work.")


part1, base_locale = solve_part1(input)
print(f"Part 1 solution: {part1}")
part2 = solve_part_2(input, base_locale)
print(f"Part 2 solution: {part2}")
