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
            3: {"name": "input", "params": 1},
            4: {"name": "output", "params": 1},
            5: {"name": "jump-if-true", "params": 2},
            6: {"name": "jump-if-false", "params": 2},
            7: {"name": "less than", "params": 3},
            8: {"name": "equals", "params": 3},
            99: {"name": "halt", "params": 0},
        }

    def load_intcode(self, intcode):
        self.memory = intcode

    def step_ahead(self, verbose=False):
        steps_to_take = 1 + self.instructions[self.opcode]["params"]
        printv(
            f"Opcode was {self.opcode} so moving ahead {steps_to_take} steps.", verbose
        )
        self.pointer += steps_to_take

    def jump(self, pos, verbose=False):
        self.pointer = pos
        printv(f"Pointer jumped to position {pos}", verbose)

    def process(self, intcode, verbose=False):
        while True:  # assuming it'll halt...
            printv(f"\nCurrently at position {self.pointer}", verbose)
            opcode, param1_mode, param2_mode, param3_mode = parse_number(
                intcode[self.pointer]
            )
            self.opcode = opcode
            printv(
                f"Current opcode: {self.opcode} ({self.instructions[self.opcode]['name']})",
                verbose,
            )

            if self.opcode == 1:  # ADD
                num1 = (
                    intcode[self.pointer + 1]  # immediate mode
                    if param1_mode == 1
                    else intcode[intcode[self.pointer + 1]]  # position mode
                )
                num2 = (
                    intcode[self.pointer + 2]  # immediate mode
                    if param2_mode == 1
                    else intcode[intcode[self.pointer + 2]]  # position mode
                )
                store_pos = intcode[self.pointer + 3]

                printv(f"Take the sum of {num1} and {num2}:", verbose)
                result = num1 + num2
                printv(result, verbose)
                printv(f"And store it at {store_pos}", verbose)
                intcode[store_pos] = result

            elif self.opcode == 2:  # MULTIPLY
                num1 = (
                    intcode[self.pointer + 1]  # immediate mode
                    if param1_mode == 1
                    else intcode[intcode[self.pointer + 1]]  # position mode
                )
                num2 = (
                    intcode[self.pointer + 2]  # immediate mode
                    if param2_mode == 1
                    else intcode[intcode[self.pointer + 2]]  # position mode
                )
                store_pos = intcode[self.pointer + 3]

                printv(f"Take the product of {num1} and {num2}:", verbose)
                result = num1 * num2
                printv(result, verbose)
                printv(f"And store it at {store_pos}", verbose)
                intcode[store_pos] = result

            elif self.opcode == 3:  # INPUT
                intake = int(input("Please input an integer: "))
                store_pos = intcode[self.pointer + 1]
                printv(
                    f"Storing input value ({intake}) at position {store_pos}", verbose
                )
                intcode[store_pos] = intake

            elif self.opcode == 4:  # OUTPUT
                # works for all examples except the "larger example" in day 5 part 2,
                # which outputs 999 in the "less than 8" case only when given
                # print(f"Output {intcode[self.pointer + 1]}") and
                # "IndexError: list index out of range" with the below. TODO: debug
                print(f"Output {intcode[intcode[self.pointer + 1]]}")

            elif self.opcode == 5:  # JUMP-IF-TRUE
                num = (
                    intcode[self.pointer + 1]  # immediate mode
                    if param1_mode == 1
                    else intcode[intcode[self.pointer + 1]]  # position mode
                )
                jump_pos = (
                    intcode[self.pointer + 2]  # immediate mode
                    if param2_mode == 1
                    else intcode[intcode[self.pointer + 2]]  # position mode
                )
                printv(f"Does {num} != 0?", verbose)
                if num != 0:
                    printv("Jump condition met", verbose)
                    self.jump(jump_pos, verbose)
                    continue
                else:
                    printv("Jump condition not met", verbose)

            elif self.opcode == 6:  # JUMP-IF-FALSE
                num = (
                    intcode[self.pointer + 1]  # immediate mode
                    if param1_mode == 1
                    else intcode[intcode[self.pointer + 1]]  # position mode
                )
                jump_pos = (
                    intcode[self.pointer + 2]  # immediate mode
                    if param2_mode == 1
                    else intcode[intcode[self.pointer + 2]]  # position mode
                )
                printv(f"Does {num} = 0?", verbose)
                if num == 0:
                    printv("Jump condition met", verbose)
                    self.jump(jump_pos, verbose)
                    continue
                else:
                    printv("Jump condition not met", verbose)

            elif self.opcode == 7:  # LESS THAN
                num1 = (
                    intcode[self.pointer + 1]  # immediate mode
                    if param1_mode == 1
                    else intcode[intcode[self.pointer + 1]]  # position mode
                )
                num2 = (
                    intcode[self.pointer + 2]  # immediate mode
                    if param2_mode == 1
                    else intcode[intcode[self.pointer + 2]]  # position mode
                )
                store_pos = intcode[self.pointer + 3]
                printv(f"Is {num1} < {num2}?", verbose)
                if num1 < num2:
                    printv("Less-than condition met", verbose)
                    printv(f"Storing value (1) at position {store_pos}", verbose)
                    intcode[store_pos] = 1
                else:
                    printv("Less-than condition not met", verbose)
                    printv(f"Storing value (0) at position {store_pos}", verbose)
                    intcode[store_pos] = 0

            elif self.opcode == 8:  # EQUALS
                num1 = (
                    intcode[self.pointer + 1]  # immediate mode
                    if param1_mode == 1
                    else intcode[intcode[self.pointer + 1]]  # position mode
                )
                num2 = (
                    intcode[self.pointer + 2]  # immediate mode
                    if param2_mode == 1
                    else intcode[intcode[self.pointer + 2]]  # position mode
                )
                store_pos = intcode[self.pointer + 3]
                printv(f"Does {num1} = {num2}?", verbose)
                if num1 == num2:
                    printv("Equality condition met", verbose)
                    printv(f"Storing value (1) at position {store_pos}", verbose)
                    intcode[store_pos] = 1
                else:
                    printv("Equality condition not met", verbose)
                    printv(f"Storing value (0) at position {store_pos}", verbose)
                    intcode[store_pos] = 0

            elif self.opcode == 99:  # HALT
                printv(f"Output at position 0: {intcode[0]}", verbose)
                printv("HALT", verbose)
                return intcode[0]

            printv(f"Intcode address 32 is currently {intcode[32]}", verbose)

            # for opcodes 5 and 6, you step ahead only if you didn't jump
            self.step_ahead(verbose)


def parse_number(number: int) -> tuple[int, int, int, int]:
    """Take in an integer of up to five digits in length and get back an
    opcode and the modes of the operation's parameters."""
    if number > 99999:
        raise Exception("Number exceeds bounds of valid parsing!")
    abcde = str(number).rjust(5, "0")
    opcode = int(abcde[3:])
    param1_mode = int(abcde[2])
    param2_mode = int(abcde[1])
    param3_mode = int(abcde[0])
    return opcode, param1_mode, param2_mode, param3_mode


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
