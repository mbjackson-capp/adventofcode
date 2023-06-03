from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2022/day/9

input = get_data(day=9, year=2022).split('\n')
input = [[line[0], int(line[2:])] for line in input]

def touching(front, back):
    '''Determines if two Knots are overlapping, adjacent, or at most one
    diagonal away from each other.'''
    return abs(front.x - back.x) <= 1 and abs(front.y -  back.y) <= 1


class Knot():
    def __init__(self):
        self.x = 0
        self.y = 0

    def catch_up_to(self, other):
        '''self is behind, other is a different Knot in front'''
        if not touching(self, other):
            if self.x < other.x:
                self.x += 1
            elif self.x > other.x:
                self.x -= 1

            if self.y < other.y:
                self.y += 1
            elif self.y > other.y:
                self.y -= 1
    

class Rope():
    def __init__(self, length):
        self.knots = [Knot() for _ in range(length)]
        self.head = self[0]
        self.tail = self[-1]
        self.visited = set()

    def __setitem__(self, index, value):
        self.knots[index] = value

    def __getitem__(self, index):
        return self.knots[index]

    def __len__(self):
        return len(self.knots)

    def __repr__(self):
        return str(len(self.visited))

    def move(self, dir, num_steps):
        '''Move head of rope in specified direction for a certain number of steps.
        With each step, update each knot later in the rope such that all knots
        continue to be touching.'''

        for _ in range(num_steps):
            if dir == 'R':
                self.head.x += 1
            elif dir == 'L':
                self.head.x -= 1
            elif dir == 'U':
                self.head.y += 1
            elif dir == 'D':
                self.head.y -= 1

            for i in range(1, len(self)):
                self[i].catch_up_to(self[i-1])
                self.visited.add((self.tail.x, self.tail.y))
        
    def move_all(self, instructions):
        '''Move rope through a list of instructions.'''
        for item in instructions:
            dir, num_steps = item
            self.move(dir, num_steps)


part1 = Rope(2)
part1.move_all(input)
print(f"Part 1 answer: {part1}")

part2 = Rope(10)
part2.move_all(input)
print(f"Part 2 answer: {part2}")