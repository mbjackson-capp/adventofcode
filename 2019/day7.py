from aocd import get_data
from computer import Computer
from itertools import permutations

input = [int(i) for i in get_data(day=7, year=2019).split(",")]

AMP_NAMES = "ABCDE"
PART1_SETTING_SEQUENCES = list(permutations(range(5)))
PART2_SETTING_SEQUENCES = list(permutations(range(5, 10)))


def find_optimal_output(setting_sequences, input=input, part=1):

    max_output_so_far = 0
    for seq in setting_sequences:
        print(f"Now trying sequence {seq}...")

        a = Computer(input)
        b = Computer(input)
        c = Computer(input)
        d = Computer(input)
        e = Computer(input)
        amps = [a, b, c, d, e]

        if part == 1:
            output_signal = part1_core(amps, seq)
        elif part == 2:
            output_signal = part2_core(amps, seq)

        if output_signal > max_output_so_far:
            print("This is higher than max output so far!")
            max_output_so_far = output_signal
            print(f"New highest output: {max_output_so_far}")
    return max_output_so_far


def part1_core(amps: list[Computer], seq: list[int]) -> int:
    """Run each amp exactly one time and return last output."""
    new_signal = 0
    for i, setting in enumerate(seq):
        print(f"Now running phase setting {setting} on amplifier {AMP_NAMES[i]}...")
        output_signal = amps[i].process(initial_inputs=[setting, new_signal])
        print(f"Output of amplifier {AMP_NAMES[i]}: {output_signal}")
        new_signal = output_signal
    print(f"Final result output: {output_signal}")
    return output_signal


def part2_core(amps: list[Computer], seq: list[int]) -> int:
    """Run amps A-E, then loop result back into A and run them again, etc.
    until all amps have halted. Then return final output from amp E"""
    new_signal = 0
    while not all([comp.status == "halted" for comp in amps]):
        for i, setting in enumerate(seq):
            if amps[i].status == "new":
                print(
                    f"Now running phase setting {setting} on amplifier {AMP_NAMES[i]}..."
                )
                output_signal = amps[i].process(
                    initial_inputs=[setting, new_signal], pause_at_output=True
                )
            else:
                print(
                    f"Now giving amplifier {AMP_NAMES[i]} input signal {new_signal}..."
                )
                output_signal = amps[i].process(
                    initial_inputs=[new_signal], pause_at_output=True
                )
            print(f"Output of amplifier {AMP_NAMES[i]}: {output_signal}")
            new_signal = output_signal
    print(f"All amps halted. Final result output: {output_signal}")
    return output_signal


if __name__ == "__main__":
    part1_solution = find_optimal_output(PART1_SETTING_SEQUENCES)
    part2_solution = find_optimal_output(PART2_SETTING_SEQUENCES, part=2)
    print(f"\nPart 1 solution: {part1_solution}")
    print(f"\nPart 2 solution: {part2_solution}")
