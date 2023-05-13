from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2021/day/1
 
input = [int(i) for i in get_data(day=1, year=2021).split('\n')]

def count_depth_increases(window: int) -> int:
    count = 0
    for i, _ in enumerate(input):
        if i >= window:
            curr_window = input[i:i-window:-1]
            prev_window = input[i-1:i-window-1:-1]
            if sum(curr_window) > sum(prev_window):
                count += 1
    return count

if __name__ == '__main__':
    print(f"The answer for part 1 is: {count_depth_increases(1)}")
    print(f"The answer for part 2 is: {count_depth_increases(3)}")