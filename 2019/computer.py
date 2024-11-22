def printv(obj, v=False):
    if v:
        print(obj)


def dictify(intcode: list[int]) -> dict:
    return {i: v for i, v in enumerate(intcode)} if intcode is not None else {}


class Computer:
    """
    Intcode computer for problems in Advent of Code 2019.
    """

    def __init__(self, intcode: list[int] | None = None, day: int | None = None):
        self.memory = dictify(intcode)
        self.ptr = 0
        self.opcode = 0
        self.day = day  # allow for day-specific modifications to procedure
        self.provided_inputs = (
            []
        )  # TODO: method to add future inputs directly to this w/o beginning processing
        self.status = "new"  # other values: "running", "paused", "halted"
        self.latest_output = None
        self.instruction_types = {
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

    def step_ahead(self, verbose=False):
        steps_to_take = 1 + self.instruction_types[self.opcode]["params"]
        printv(
            f"Opcode was {self.opcode} so moving pointer ahead {steps_to_take} steps.",
            verbose,
        )
        self.ptr += steps_to_take

    def jump(self, pos, verbose=False):
        self.ptr = pos
        printv(f"Pointer jumped to position {pos}", verbose)

    def process(
        self,
        intcode: list[int] | None = None,
        initial_inputs: list[int] | None = None,
        pause_at_output: bool = False,
        verbose: bool = False,
    ):
        if len(self.memory) == 0:
            self.memory = dictify(intcode)
            printv(f"Memory overwritten with new intcode: {intcode}", verbose)

        self.status = "running"
        if initial_inputs is not None:
            self.provided_inputs = initial_inputs
        while self.status != "halted":
            printv(f"\nCurrently at position {self.ptr}", verbose)
            opcode, param1_mode, param2_mode, param3_mode = parse_number(
                self.memory[self.ptr]
            )
            self.opcode = opcode
            printv(
                f"Current opcode: {self.opcode} ({self.instruction_types[self.opcode]['name']})",
                verbose,
            )

            if self.opcode == 1:  # ADD
                num1 = (
                    self.memory[self.ptr + 1]  # immediate mode
                    if param1_mode == 1
                    else self.memory[self.memory[self.ptr + 1]]  # position mode
                )
                num2 = (
                    self.memory[self.ptr + 2]  # immediate mode
                    if param2_mode == 1
                    else self.memory[self.memory[self.ptr + 2]]  # position mode
                )
                store_pos = self.memory[self.ptr + 3]

                printv(f"Take the sum of {num1} and {num2}:", verbose)
                result = num1 + num2
                printv(result, verbose)
                printv(f"And store it at {store_pos}", verbose)
                self.memory[store_pos] = result

            elif self.opcode == 2:  # MULTIPLY
                num1 = (
                    self.memory[self.ptr + 1]  # immediate mode
                    if param1_mode == 1
                    else self.memory[self.memory[self.ptr + 1]]  # position mode
                )
                num2 = (
                    self.memory[self.ptr + 2]  # immediate mode
                    if param2_mode == 1
                    else self.memory[self.memory[self.ptr + 2]]  # position mode
                )
                store_pos = self.memory[self.ptr + 3]

                printv(f"Take the product of {num1} and {num2}:", verbose)
                result = num1 * num2
                printv(result, verbose)
                printv(f"And store it at {store_pos}", verbose)
                self.memory[store_pos] = result

            elif self.opcode == 3:  # INPUT
                if len(self.provided_inputs) > 0:
                    # consume pre-provided inputs as long as there are any
                    intake = self.provided_inputs.pop(0)
                else:
                    intake = int(input("Please input an integer: "))
                store_pos = self.memory[self.ptr + 1]
                printv(
                    f"Storing input value ({intake}) at position {store_pos}", verbose
                )
                self.memory[store_pos] = intake

            elif self.opcode == 4:  # OUTPUT
                # works for all examples except the "larger example" in day 5 part 2,
                # which outputs 999 in the "less than 8" case only when given
                # print(f"Output {self.memory[self.ptr + 1]}") and
                # "IndexError: list index out of range" with the below. TODO: debug
                thing_outputted = self.memory[self.memory[self.ptr + 1]]
                print(f"Output {thing_outputted}")
                self.latest_output = thing_outputted

            elif self.opcode == 5:  # JUMP-IF-TRUE
                num = (
                    self.memory[self.ptr + 1]  # immediate mode
                    if param1_mode == 1
                    else self.memory[self.memory[self.ptr + 1]]  # position mode
                )
                jump_pos = (
                    self.memory[self.ptr + 2]  # immediate mode
                    if param2_mode == 1
                    else self.memory[self.memory[self.ptr + 2]]  # position mode
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
                    self.memory[self.ptr + 1]  # immediate mode
                    if param1_mode == 1
                    else self.memory[self.memory[self.ptr + 1]]  # position mode
                )
                jump_pos = (
                    self.memory[self.ptr + 2]  # immediate mode
                    if param2_mode == 1
                    else self.memory[self.memory[self.ptr + 2]]  # position mode
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
                    self.memory[self.ptr + 1]  # immediate mode
                    if param1_mode == 1
                    else self.memory[self.memory[self.ptr + 1]]  # position mode
                )
                num2 = (
                    self.memory[self.ptr + 2]  # immediate mode
                    if param2_mode == 1
                    else self.memory[self.memory[self.ptr + 2]]  # position mode
                )
                store_pos = self.memory[self.ptr + 3]
                printv(f"Is {num1} < {num2}?", verbose)
                if num1 < num2:
                    printv("Less-than condition met", verbose)
                    printv(f"Storing value (1) at position {store_pos}", verbose)
                    self.memory[store_pos] = 1
                else:
                    printv("Less-than condition not met", verbose)
                    printv(f"Storing value (0) at position {store_pos}", verbose)
                    self.memory[store_pos] = 0

            elif self.opcode == 8:  # EQUALS
                num1 = (
                    self.memory[self.ptr + 1]  # immediate mode
                    if param1_mode == 1
                    else self.memory[self.memory[self.ptr + 1]]  # position mode
                )
                num2 = (
                    self.memory[self.ptr + 2]  # immediate mode
                    if param2_mode == 1
                    else self.memory[self.memory[self.ptr + 2]]  # position mode
                )
                store_pos = self.memory[self.ptr + 3]
                printv(f"Does {num1} = {num2}?", verbose)
                if num1 == num2:
                    printv("Equality condition met", verbose)
                    printv(f"Storing value (1) at position {store_pos}", verbose)
                    self.memory[store_pos] = 1
                else:
                    printv("Equality condition not met", verbose)
                    printv(f"Storing value (0) at position {store_pos}", verbose)
                    self.memory[store_pos] = 0

            elif self.opcode == 99:  # HALT
                printv(f"Output at position 0: {self.memory[0]}", verbose)
                printv("HALT", verbose)
                self.status = "halted"
                if self.day == 2:
                    return self.memory[0]
                else:
                    return self.latest_output

            # for opcodes 5 and 6, you step ahead only if you didn't jump
            self.step_ahead(verbose)

            if self.opcode == 4 and pause_at_output:
                self.status = "paused"
                return self.latest_output


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
