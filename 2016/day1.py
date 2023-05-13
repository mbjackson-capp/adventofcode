from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2016/day/1

input = get_data(day=1, year=2016).split(', ')

DIRS = "NESW"

class Car():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.heading = 'N'
        self.visited = set()
        self.visited_a_pt_2x = False
    
    def turn(self, dir: str):
        '''
        Turn the car right or left.
        '''
        if dir == 'L':
            self.heading = DIRS[(DIRS.index(self.heading) - 1) % 4]
        elif dir == 'R':
            self.heading = DIRS[(DIRS.index(self.heading) + 1) % 4]
    
    def move(self, dist: int):
        '''
        Move car through all blocks in the direction it's headed.
        '''
        if self.heading == 'N':
            blocks_visited = [(self.x, self.y+block) for block in range(1, dist+1)]
        elif self.heading == 'S':
            blocks_visited = [(self.x, self.y-block) for block in range(1, dist+1)]
        elif self.heading == 'E':
            blocks_visited = [(self.x+block, self.y) for block in range(1, dist+1)]
        elif self.heading == 'W':
            blocks_visited = [(self.x-block, self.y) for block in range(1, dist+1)]
        
        for block in blocks_visited:
            if block in self.visited and not self.visited_a_pt_2x:
                print(f'{block} is the first point visited twice!')
                self.visited_a_pt_2x = True
                print(f"That's {abs(block[0]) + abs(block[1])} blocks away (part 2)")
            self.visited.add(block)
        
        #set Car location to end of the stretch it just drove
        self.x = blocks_visited[-1][0]
        self.y = blocks_visited[-1][1]
    
def drive():
    car = Car()
    for line in input: 
        dir = line[0] #can't do tuple unpacking because number length varies
        dist = int(line[1:])
        car.turn(dir)
        car.move(dist)
    return car.x + car.y

if __name__ == '__main__':
    print(f"Car drove to a point {drive()} blocks from start (part 1)")