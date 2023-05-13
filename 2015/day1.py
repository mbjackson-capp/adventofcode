from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2015/day/1

input = get_data(day=1, year=2015)

curr_floor = 0
visited_basement = False
for pos, paren in enumerate(input):
    if paren == '(':
        curr_floor += 1
    elif paren == ')':
        curr_floor -= 1
    
    if curr_floor == -1 and not visited_basement:
        visited_basement = True
        print(f"Santa first entered basement at position {pos+1} (part 2)")

print(f"Instructions took Santa to floor {curr_floor} (part 1)")