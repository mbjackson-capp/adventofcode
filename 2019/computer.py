def printv(obj, v=False):
    if v:
        print(obj)


class Computer:
    """
    Intcode computer for problems in Advent of Code 2019.
    """

    def __init__(self, intcode=None):
        self.pointer = 0
        self.opcode = 0
        self.memory = intcode  # Intcode object goes here
        self.instructions = {
            1: {"name": "add", "params": 3},
            2: {"name": "multiply", "params": 3},
            99: {"name": "halt", "params": 0},
        }

    def load_intcode(self, intcode):
        self.memory = intcode

    def step_ahead(self):
        self.pointer += 1 + self.instructions[self.opcode]["params"]

    def process(self, intcode, verbose=False):
        while True:  # assuming it'll halt...
            printv(f"\nCurrently at position {self.pointer}", verbose)
            self.opcode = intcode[self.pointer]
            printv(
                f"Current opcode: {self.opcode} ({self.instructions[self.opcode]['name']})",
                verbose,
            )

            if self.opcode == 1:  # ADD
                num1 = intcode[self.pointer + 1]
                num2 = intcode[self.pointer + 2]
                store_pos = intcode[self.pointer + 3]

                printv(f"Take the sum of positions {num1} and {num2}:", verbose)
                result = intcode[num1] + intcode[num2]
                printv(result, verbose)
                printv(f"And store it at {store_pos}", verbose)
                intcode[store_pos] = result

            elif self.opcode == 2:  # MULTIPLY
                num1 = intcode[self.pointer + 1]
                num2 = intcode[self.pointer + 2]
                store_pos = intcode[self.pointer + 3]

                printv(f"Take the product of positions {num1} and {num2}:", verbose)
                result = intcode[num1] * intcode[num2]
                printv(result, verbose)
                printv(f"And store it at {store_pos}", verbose)
                intcode[store_pos] = result

            elif self.opcode == 99:  # HALT
                printv(f"Output at position 0: {intcode[0]}", verbose)
                return intcode[0]

            self.step_ahead()


class Intcode:
    """In progress, not currently used"""

    def __init__(self, numlist):
        self.code = numlist
        # TODO: put some asserts here to make sure all entries are numbers
        if 99 not in self.intcode:
            print("Warning: this intcode doesn't contain 99 -- may fail to halt")

    # make sure that however you implement this, a reset is possible
    def provide_inputs(self, noun, verb):
        self.code[1] = noun
        self.code[2] = verb
