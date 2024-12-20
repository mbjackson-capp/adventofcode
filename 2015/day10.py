example = "1"
# Replace with your input
input = "1321131112"

def look_say(intstr: str) -> str:
    """Perform a single instance of the look-and-say game. See problem statement."""
    new_intstr = ""
    digits = [int(i) for i in intstr]
    for ix, digit in enumerate(digits):
        if ix == 0:
            repetitions = 1
            prev_digit = digit
        elif prev_digit == digit:
            repetitions += 1
        else:
            new_intstr += str(repetitions)
            new_intstr += str(prev_digit)
            repetitions = 1
            prev_digit = digit
    new_intstr += str(repetitions)
    new_intstr += str(prev_digit)
    return new_intstr


def run(input, steps=40):
    """Perform consecutive instances of the look-and-say game, feeding the output
    of one step in as the input of the next step.
    NOTE: This 'naive' approach works fine for the necessary 50 steps, but begins
    to struggle around step 45 and is not suitable for numbers of steps much higher
    than that. 
    TODO: Find a 'closed form' solution with more efficient runtime complexity."""
    for step in range(steps):
        print(f"Now calculating step {step}...")
        input = look_say(input)
        print(f"Length at this step: {len(input)}")
    return len(input), input

if __name__ == '__main__':
    part1_solution, input_after_40 = run(input)
    print(f"Part 1 solution: {part1_solution}")
    part2_solution, _ = run(input_after_40, steps=10)
    print(f"Part 2 solution: {part2_solution}")