from aocd import get_data
from typing import List, Tuple
from shapely import Polygon

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2025/day/9


def get_red_tiles(data: str) -> List[Tuple[int, int]]:
    data = [row for row in data.split("\n")]
    data = [tuple(int(j) for j in entry.split(",")) for entry in data]
    return data


def part1(data: str) -> int:
    """Find the biggest possible area of a rectangle with two red tiles
    at diagonally opposite corners. Uses naive O(n^2) approach to check
    every possible pair; TODO: figure out a speedup?"""
    tiles = get_red_tiles(data)
    max_area = 0
    for i, tile1 in enumerate(tiles):
        for j in range(i + 1, len(tiles)):
            tile2 = tiles[j]
            x1, y1 = tile1
            x2, y2 = tile2
            # Note that tiles along same horizontal or vertical line
            # produce a rectangle of width 1, per problem statement
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if area > max_area:
                max_area = area
    return max_area


def part2(data: str) -> int:
    """Find the biggest possible area of a rectangle with two red tiles
    at diagonally opposite corners, and its entire area within tiles that are
    red or green. Uses naive O(n^2) approach to check every possible pair;
    TODO: figure out a speedup?"""
    tiles = get_red_tiles(data)
    green_perimeter = Polygon(tiles)
    max_area = 0
    for i, tile1 in enumerate(tiles):
        for j in range(i + 1, len(tiles)):
            tile2 = tiles[j]
            x1, y1 = tile1
            x2, y2 = tile2
            corner3 = (x1, y2)
            corner4 = (x2, y1)
            coords = [tile1, corner3, tile2, corner4]
            # NOTE: rect.area method is not defined the same way as tile
            # rectangle area is in problem statement, so you can't call
            # rect.area directly. But shapely's .contains() method will
            # still have the proper truth value
            rect = Polygon(coords)
            if green_perimeter.contains(rect):
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                if area > max_area:
                    max_area = area
    return max_area


if __name__ == "__main__":
    input_data = get_data(day=9, year=2025)
    ans1 = part1(input_data)
    print(f"Part 1 answer: {ans1}")
    print(f"Now calculating Part 2...This could take a few seconds...")
    ans2 = part2(input_data)
    print(f"Part 2 answer: {ans2}")
