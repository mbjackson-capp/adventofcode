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
        self.relative_base = 0
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
            9: {"name": "adjust-relative-base", "params": 1},
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

    def value(self, param: int, mode: int):
        if mode == 0:  # position mode
            addr = self.memory[self.ptr + param]
        elif mode == 1:  # immediate mode
            addr = self.ptr + param
        elif mode == 2:  # relative mode
            addr = self.relative_base + self.memory[self.ptr + param]
        try:
            return self.memory[addr]
        except KeyError:  # far-off memory always initializes at 0
            self.memory[addr] = 0
            return self.memory[addr]

    def process(
        self,
        intcode: list[int] | None = None,
        initial_inputs: list[int] | None = None,
        pause_at_output: bool = False,
        verbose: bool = False,
    ):
        if intcode is not None:
            self.memory = dictify(intcode)
            printv(f"Memory overwritten with new intcode: {intcode}", verbose)
            printv(self.memory, verbose)

        if self.status == "new":
            self.ptr = 0
            printv(f"Pointer reset to {self.ptr}", verbose)
            self.relative_base = 0
            printv(f"Relative base reset to {self.relative_base}", verbose)
        self.status = "running"
        if initial_inputs is not None:
            self.provided_inputs = initial_inputs
        while self.status != "halted":
            printv(f"\nCurrently at position {self.ptr}", verbose)
            printv(f"Value at position {self.ptr}: {self.memory[self.ptr]}", verbose)
            opcode, param1_mode, param2_mode, param3_mode = parse_number(
                self.memory[self.ptr]
            )
            printv(
                f"Outputs of parse_number: {opcode, param1_mode, param2_mode, param3_mode}",
                verbose,
            )
            self.opcode = opcode
            printv(
                f"Current opcode: {self.opcode} ",
                verbose,
            )
            printv(({self.instruction_types[self.opcode]["name"]}), verbose)

            if self.opcode == 1:  # ADD
                num1 = self.value(param=1, mode=param1_mode)
                num2 = self.value(param=2, mode=param2_mode)
                store_pos = self.memory[self.ptr + 3]

                printv(f"Take the sum of {num1} and {num2}:", verbose)
                result = num1 + num2
                printv(result, verbose)
                printv(f"And store it at position {store_pos}", verbose)
                self.memory[store_pos] = result

            elif self.opcode == 2:  # MULTIPLY
                num1 = self.value(param=1, mode=param1_mode)
                num2 = self.value(param=2, mode=param2_mode)
                store_pos = self.memory[self.ptr + 3]

                printv(f"Take the product of {num1} and {num2}:", verbose)
                result = num1 * num2
                printv(result, verbose)
                printv(f"And store it at position {store_pos}", verbose)
                self.memory[store_pos] = result

            elif self.opcode == 3:  # INPUT
                if len(self.provided_inputs) > 0:
                    # consume pre-provided inputs as long as there are any
                    intake = self.provided_inputs.pop(0)
                else:
                    intake = int(input("Please input an integer: "))
                # if param1_mode == 1:
                #     raise ValueError(
                #         "Parameters that an instruction writes to will never be in immediate mode"
                #     )
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
                printv(f"Mode {param1_mode}", verbose)
                thing_outputted = self.value(param=1, mode=param1_mode)
                print(f"Output {thing_outputted}")
                self.latest_output = thing_outputted

            elif self.opcode == 5:  # JUMP-IF-TRUE
                num = self.value(param=1, mode=param1_mode)
                jump_pos = self.value(param=2, mode=param2_mode)
                printv(f"Does {num} != 0?", verbose)
                if num != 0:
                    printv("Jump condition met", verbose)
                    self.jump(jump_pos, verbose)
                    continue
                else:
                    printv("Jump condition not met", verbose)

            elif self.opcode == 6:  # JUMP-IF-FALSE
                num = self.value(param=1, mode=param1_mode)
                jump_pos = self.value(param=2, mode=param2_mode)
                printv(f"Does {num} = 0?", verbose)
                if num == 0:
                    printv("Jump condition met", verbose)
                    self.jump(jump_pos, verbose)
                    continue
                else:
                    printv("Jump condition not met", verbose)

            elif self.opcode == 7:  # LESS THAN
                num1 = self.value(param=1, mode=param1_mode)
                num2 = self.value(param=2, mode=param2_mode)
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
                num1 = self.value(param=1, mode=param1_mode)
                num2 = self.value(param=2, mode=param2_mode)
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

            elif self.opcode == 9:  # ADJUST RELATIVE BASE
                adjust_amt = self.value(param=1, mode=param1_mode)
                printv(
                    f"Adjusting relative base {self.relative_base} by amount {adjust_amt}...",
                    verbose,
                )
                self.relative_base += adjust_amt
                printv(f"Relative base is now {self.relative_base}", verbose)

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
