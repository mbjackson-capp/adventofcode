from aocd import get_data
from copy import deepcopy
import numpy as np
from collections import Counter

input = [int(i) for i in get_data(day=8, year=2019)]

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


def build_layers(nums=input, width=IMAGE_WIDTH, height=IMAGE_HEIGHT):
    layers = []
    blank_layer = [[None for i in range(width)] for j in range(height)]
    while len(nums) > 0:
        layer_in_progress = deepcopy(blank_layer)
        for j in range(height):
            for i in range(width):
                this_digit = nums.pop(0)
                layer_in_progress[j][i] = this_digit
        layers.append(np.array(layer_in_progress, dtype=int))
    return layers


def part1(layers, w=IMAGE_WIDTH, h=IMAGE_HEIGHT):
    zeros_count_by_layer = {}
    fewest_zeros_so_far = w * h
    fewest_zeros_layer_idx = 0
    for i, layer in enumerate(layers):
        zeros_on_this_layer = Counter(layer.flatten())[np.int64(0)]
        zeros_count_by_layer[i] = zeros_on_this_layer
        if zeros_on_this_layer < fewest_zeros_so_far:
            fewest_zeros_so_far = zeros_on_this_layer
            fewest_zeros_layer_idx = i

    target_layer_counter = Counter(layers[fewest_zeros_layer_idx].flatten())
    return target_layer_counter[np.int64(1)] * target_layer_counter[np.int64(2)]


def first_zero_or_one(arr):
    for _, item in enumerate(arr):
        if item in [0, 1]:
            return item


def part2(layers):
    layers = np.array(layers)
    ans = np.apply_along_axis(first_zero_or_one, 0, layers)
    for row in ans:
        print(row)


example = [int(i) for i in "0222112222120000"]

if __name__ == "__main__":
    layers = build_layers(input)
    print(f"Part 1 solution: {part1(layers)}")
    print(f"Part 2 solution (ctrl-F the number 1 to see letters clearly):\n")
    part2(layers)
