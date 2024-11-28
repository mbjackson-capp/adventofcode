from aocd import get_data
import re
from itertools import combinations
import sys


class Moon:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0):
        self.pos = [x, y, z]
        self.vel = [0, 0, 0]

    def __repr__(self):
        x, y, z = self.pos
        x_vel, y_vel, z_vel = self.vel
        return f"<pos=x= {x}, y= {y}, z= {z}>, vel=<x= {x_vel}, y= {y_vel}, z= {z_vel}>"

    def apply_velocity(self):
        for ix in range(3):
            self.pos[ix] += self.vel[ix]

    def energy(self):
        pot = sum([abs(axis_pos) for axis_pos in self.pos])
        kin = sum([abs(axis_vel) for axis_vel in self.vel])
        tot = pot * kin
        return pot, kin, tot


def parse_new_moon(moon_str: str) -> Moon:
    """Turn a representation like <x=17, y=-7, z=-11> into a Moon object"""
    digits = re.findall(r"-?\d+", moon_str)
    this_x = int(digits[0])
    this_y = int(digits[1])
    this_z = int(digits[2])
    return Moon(x=this_x, y=this_y, z=this_z)


def apply_gravity_pair(moon_a: Moon, moon_b: Moon):
    COORD_INDICES = [0, 1, 2]
    for idx in COORD_INDICES:
        if moon_a.pos[idx] == moon_b.pos[idx]:
            continue
        else:  # bring moons closer on current axis
            if moon_a.pos[idx] > moon_b.pos[idx]:
                moon_a.vel[idx] -= 1
                moon_b.vel[idx] += 1
            elif moon_a.pos[idx] < moon_b.pos[idx]:
                moon_a.vel[idx] += 1
                moon_b.vel[idx] -= 1


def do_timestep(moon_list: list[Moon]):
    moon_pairs = combinations(
        moon_list, 2
    )  # relies on list referencing to point to same object, not copy
    for pair in moon_pairs:
        moon_a, moon_b = pair
        apply_gravity_pair(moon_a, moon_b)
    for moon in moon_list:
        moon.apply_velocity()


def simulate_moon_system(
    moon_list: list[Moon], last_step=10, print_after_every=1, print_energy=True
):
    cur_step = 0
    for _ in range(last_step):
        cur_step += 1
        do_timestep(moon_list)
        if (print_after_every is not None) and (cur_step % print_after_every) == 0:
            print(f"\nAfter {cur_step} steps:")
            for moon in moon_list:
                print(moon)
    if print_energy:
        print(f"\nEnergy after {cur_step} steps:")
    total_energies = []
    for moon in moon_list:
        pot, kin, tot = moon.energy()
        total_energies.append(tot)
        if print_energy:
            print(f"pot: {pot}, kin: {kin}, total: {pot} * {kin} = {tot}")
    te_sum = sum(total_energies)
    if print_energy:
        print(f"Sum of total energy: {te_sum}")
    return te_sum


def state_string(moon_list: list[Moon]):
    result = ""
    for moon in moon_list:
        result += repr(moon)
    return result


example_1 = [
    parse_new_moon(i)
    for i in """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""".split(
        "\n"
    )
]

example_2 = [
    parse_new_moon(i)
    for i in """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""".split(
        "\n"
    )
]


def part1():
    input = [parse_new_moon(i) for i in get_data(day=12, year=2019).split("\n")]
    part1 = simulate_moon_system(
        input, last_step=1000, print_after_every=None, print_energy=False
    )
    print(f"Part 1 solution: {part1}")


def part2_slow(
    input=[parse_new_moon(i) for i in get_data(day=12, year=2019).split("\n")],
    print_after_every=100_000,
):
    """Proof of concept. Takes about 7 seconds per million time steps; to
    reach 4.6 billion timesteps like example 2, it'd take about 32800 seconds,
    i.e. about 9 hours. It also looks as though the set of state strings reaches
    4GB after about 80 million steps. We need to do better than this."""
    previous_states = set()
    # could hash or convert down the strings to save memory I suppose
    t = 0
    while True:
        do_timestep(input)
        cur_state = state_string(input)
        if cur_state in previous_states:
            return t
        else:
            previous_states.add(cur_state)
        t += 1
        if t % print_after_every == 0:
            print(t)
            # print(f"Size of cur_states: {sys.getsizeof(previous_states) / 1_000_000} MB")


if __name__ == "__main__":
    part1()
    # part2 = part2_slow(input=example_2)
    # print(f"Part 2 solution: {part2}")
