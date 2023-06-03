from aocd import get_data
#set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

#Problem statement: https://adventofcode.com/2022/day/10

input = get_data(day=10, year=2022).split('\n')

CHECK_CYCLES = [20 + (40 * i) for i in range(6)]
CRT_WIDTH = 40

class Cpu:
    def __init__(self):
        self.X = 1
        self.cycle = 0
        self.crt = []
        self.signal_strengths = []
        self.curr_row = ''

    def addx(self, int):
        for _ in range(2):
            self.cycle += 1
            self.cycle_check()
        self.X += int

    def noop(self):
        self.cycle += 1
        self.cycle_check()

    def cycle_check(self):
        #part 1
        if self.cycle in CHECK_CYCLES:
            self.signal_strengths.append(self.cycle * self.X)

        #part 2
        sprite = [self.X-1, self.X, self.X+1]
        pos = (self.cycle - 1) % CRT_WIDTH
        if pos in sprite:
            self.curr_row += '#'
        else:
            self.curr_row += '.'

        if self.cycle % CRT_WIDTH == 0:
            self.crt.append(self.curr_row)
            self.curr_row = ''

    def display(self):
        for line in self.crt:
            print(line)

    def run(self, instructions):
        for line in instructions:
            OP_END = 4
            op = line[:OP_END]
            if op == 'noop':
                self.noop()
            elif op == 'addx':
                NUM_START = 5
                num = int(line[NUM_START:])
                self.addx(num)
        
        print(f"Part 1 answer: {sum(self.signal_strengths)}")
        print("Part 2 answer:")
        self.display()

part1_cpu = Cpu()
part1_cpu.run(input)
