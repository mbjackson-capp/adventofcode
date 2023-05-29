from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1
import re
import time
from collections import Counter

#Problem statement: https://adventofcode.com/2021/day/12

input = get_data(day=12, year=2021).split('\n')

def build_paths(segments, paths_so_far=[], part=1):
    #starting case
    if not paths_so_far:
        paths_so_far = [start_first(s) for s in segments if 'start' in s]
        non_start_segments = [s for s in segments if not 'start' in s]
        return build_paths(non_start_segments, paths_so_far, part)

    #final case
    if paths_so_far == [path for path in paths_so_far if '-end' in path]:
        return paths_so_far

    #recursive case
    else:
        new_paths = []
        for path in paths_so_far:
            old_path = path
            if '-end' in path:
                new_paths.append(path)
            else:
                last_cave = re.split('-', path)[-1]
                for segment in segments:
                    seg_set = {cave for cave in re.split('-', segment)}
                    if last_cave in seg_set:
                        next_cave = (seg_set - {last_cave}).pop()
                        if (next_cave == next_cave.upper() or
                            (part == 1 and next_cave not in old_path) or
                            (part == 2 and (next_cave == 'end' or 
                                           (not saw_a_small_cave_twice(old_path) or 
                                            next_cave not in old_path)))):
                            new_path = old_path + f'-{next_cave}'
                            new_paths.append(new_path)
        return build_paths(segments, paths_so_far=new_paths, part=part)

def saw_a_small_cave_twice(path):
    small_caves = re.findall('(start|-[a-z]+)', path)
    return len(small_caves) != len(set(small_caves))

#path segments are bidirectional but actual path must start with 'start'
def start_first(segment):
    if '-start' in segment:
        segment = 'start-' + re.sub('-start', '', segment)
    return segment

def run(segments, pt=1):
    all_paths = [re.sub(r'start-(.+)-end', r'\1', i) 
                 for i in build_paths(segments, part=pt)]
    if pt == 1:
        small_cave_paths = [i for i in all_paths if re.search('[a-z]', i)]
        return len(small_cave_paths)
    else:
        return len(all_paths)


if __name__ == '__main__':
    print(f"Part 1 solution: {run(input, pt=1)}")
    print(f"Part 2 solution: {run(input, pt=2)}") #takes about 7 seconds
