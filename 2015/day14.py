from aocd import get_data
from dataclasses import dataclass
from typing import List
import re

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1


class Reindeer:
    def __init__(self, name, speed, max_fly_time, max_rest_time):
        self.dist = 0
        self.clock = 0
        self.timer = 0
        self.points = 0
        self.resting = False
        self.name = name
        self.speed = speed
        self.max_fly_time = max_fly_time
        self.max_rest_time = max_rest_time

    def next_second(self):
        self.clock += 1
        self.timer += 1
        if not self.resting:
            self.dist += self.speed
            if self.timer == self.max_fly_time:
                self.resting = True
                self.timer = 0
        if self.resting and self.timer == self.max_rest_time:
            self.resting = False
            self.timer = 0

    def __repr__(self):
        return (
            f"{self.name}: {self.dist}km after {self.clock} sec, "
            f"{'resting' if self.resting else 'flying'} for {self.timer} sec "
            f"(points: {self.points})"
        )

    def __str__(self):
        return self.name


def parse_reindeer(r_str: str) -> Reindeer:
    assert (
        "can fly" in r_str and "but then must rest for" in r_str
    ), f"{r_str} not a valid reindeer string"
    name = r_str.split(" ")[0]
    speed, max_fly_time, max_rest_time = [int(i) for i in re.findall(r"\d+", r_str)]
    return Reindeer(name, speed, max_fly_time, max_rest_time)


def parse_input(data: str) -> List[Reindeer]:
    return [parse_reindeer(line) for line in data.split("\n")]


@dataclass
class Race:
    racers: List[Reindeer]
    clock: int = 0

    @property
    def leader(self):
        order_of_finish = sorted(self.racers, key=lambda r: r.dist, reverse=True)
        return order_of_finish[0]

    @property
    def winner(self):
        order_of_points = sorted(self.racers, key=lambda r: r.points, reverse=True)
        return order_of_points[0]

    def advance(self, n_seconds: int):
        for _ in range(n_seconds):
            self.clock += 1
            for r in self.racers:
                r.next_second()
            self.leader.points += 1


def solve(data: str, n_seconds: int = 2503, part=1):
    race = Race(parse_input(data))
    race.advance(n_seconds)
    return race.leader.dist if part == 1 else race.winner.points


if __name__ == "__main__":
    input = get_data(day=14, year=2015)
    print(f"Part 1 answer: {solve(input, part=1)}")
    print(f"Part 2 answer: {solve(input, part=2)}")
