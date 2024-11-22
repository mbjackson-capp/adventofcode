from math import gcd

# TODO: get input with AOCD library
map_input = [[char for char in row] for row in input.split("\n")]

START = (2,2)

def slope(x1, y1, x2, y2):
    try:
        return (y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
        if y2 > y1:
            return float("inf")
        else: 
            return float("-inf")

def detector_sweep(mp, start: tuple[int, int], part=1):
    """Sweep around an asteroid to detect all other asteroids around it.
    TODO: fix this so it always starts up and does a full loop clockwise
    TODO: use numpy array instead of list of lists"""
    slopes_swept = set()
    asteroids_detected = []
    start_x = start[0]
    start_y = start[1]
    # print(f"SWEEPING FROM POINT {start_y, start_x}")
    width_x = len(mp)
    width_y = len(mp[0])
    
    left_dist = -start_x
    right_dist = width_x - start_x
    up_dist = -start_y
    down_dist = width_y - start_y
    for dx in range(left_dist, right_dist):
        for dy in range(up_dist, down_dist):
            if (dx == 0 and dy == 0):
                continue
            x = start_x 
            y = start_y
            # print(f"New increment: {dx, dy}")
            # normalize increment to nearest terms
            inc_x = int(dx / gcd(dx, dy))
            inc_y = int(dy / gcd(dx, dy))
            m = (inc_x, inc_y)
            # print(f"Slope: {m}")
            if m in slopes_swept:
                # This slope has already been swept! Skipping
                continue
            slopes_swept.add(m)
            while (0 <= x < width_x) and (0 <= y < width_y):
                # normalize increments to simplest terms
                x += inc_x
                y += inc_y 
                # print(x, y)
                if (x < 0) or (x >= width_x) or (y < 0) or (y >= width_x):
                    # Sweep hit end of map! On to the next sweep angle
                    break
                # print(f"Checking {x, y} for asteroid...")
                if mp[y][x] == '#':
                    # Asteroid detected at {x,y}! On to the next sweep angle"
                    if (x,y) not in asteroids_detected:
                        asteroids_detected.append((x,y))
                        # TODO: if part == 2, change mp[y][x] to 'v'
                    # skip over asteroids already detected by a previous sweep
                    break 
            
    # print(f"Set of asteroids detected: {asteroids_detected}")
    # print(f"There are {len(asteroids_detected)} of them")
    # get the list of valid increment-directions to do FIRST, and THEN run through them
    # print(f"Slopes swept: {sorted(sorted(list(slopes_swept), key=lambda y:y[1]), key=lambda x:x[0])}")
    return asteroids_detected

def sweep_all(mp):
    width_x = len(mp)
    width_y = len(mp[0])
    results = {}
    for x in range(width_x):
        for y in range(width_y):
            if mp[y][x] == '.': # Can't build a base at {x,y} - no asteroid to build on!"
                continue 
            elif mp[y][x] == '#':
                result = len(detector_sweep(mp, (x,y)))
                results[result] = (x,y) # save coordinates of asteroid
    return max(results.keys()), results[max(results.keys())]
    
part1, _ = sweep_all(map_input)
print(f"Part 1 solution: {part1}")


# Possible sweep order, part 1:
# TODO: change order so it goes around by angle (you can use trig to calculate angle from (0,0) unit circle and then sort list of angles by that, starting from 90 and going backwards to -90)
# -1dx, 0dy: nothing
# -1dx, 1dy: nothing
# -1dx, 2dy: (0, 2)
# -1dx, 3dy: nothing
# -1dx, 4dy: nothing
# 0dx, 0dy: SKIP (no movement)  
# 0dx, 1dy: (1, 2) <-- START SWEEP HERE, SOMEHOW
# 0dx 2dy: SKIP (slope already investigated as 0dx, 1dy)
# 0dx 3dy: SKIP (slope already investigated as 0dx, 1dy)
# 0dx 4dy: SKIP (slope already investigated as 0dx, 1dy)
# 1dx, 0dy: (4, 0) 
# 1dx, 1dy: (2, 3)
# 1dx, 2dy: (2, 2)
# 1dx, 3dy: nothing
# 1dx, 4dy: nothing
# 2dx, 0dy: SKIP (slope already investigated as 1dx, 0dy)
# 2dx, 1dy: nothing
# 2dx, 2dy: SKIP (slope already investigated as 1dx, 1dy)
# 2dx, 3dy: nothing
# 2dx, 4dy: SKIP (slope already investigated as 1dx, 2dy)
# 3dx, 0dy: SKIP (slope already investigated)
# 3dx, 1dy: nothing
# 3dx, 2dy: (4, 2)
# 3dx, 3dy: SKIP (alope already investigated as 1dx, 1dy)
# 3dx, 4dy: (4, 4)
# <-- LOOP AROUND TO THE HIGHEST-MAGNITUDE NEGATIVE NUMBER AND KEEP GOING UP
