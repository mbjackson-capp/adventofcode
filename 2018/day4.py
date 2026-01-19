from aocd import get_data
import re
import pandas as pd
from itertools import batched

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

# Problem statement: https://adventofcode.com/2018/day/4


def parse_record(record: str):
    time_part, desc = re.split(r"\]\s", record)
    year, month, day, hour, minute = [int(i) for i in re.findall(r"\d+", time_part)]
    time = (year, month, day, hour, minute)
    return (time, desc)


def assemble_table(data: str):
    records = [parse_record(record) for record in data.split("\n")]
    records = sorted(records, key=lambda i: i[0])
    record_dict = {}
    for record in records:
        time, desc = record
        _, month, day, _, minute = time
        if "Guard #" in desc:
            guard = int(re.search(r"\d+", desc).group())
        else:  # assumes 'falls asleep' is always followed by a 'wakes up'
            date = (month, day)
            if date not in record_dict:
                record_dict[date] = {"guard": guard, "ranges": []}
            record_dict[date]["ranges"].append(minute)
    for date in record_dict.keys():
        # get ranges of time asleep
        range_batch = batched(record_dict[date]["ranges"], 2)
        actual_ranges = [range(r[0], r[1]) for r in range_batch]
        record_dict[date]["ranges"] = actual_ranges

    # initialize table as shown in problem statement
    df = pd.DataFrame()
    df["month"] = [k[0] for k in record_dict.keys()]
    df["day"] = [k[1] for k in record_dict.keys()]
    df = df.set_index(["month", "day"])
    df["guard"] = [record_dict[k]["guard"] for k in record_dict]
    for minute in range(60):
        df[f"{minute}"] = 0
    for date in record_dict.keys():
        month, day = date
        ranges = record_dict[date]["ranges"]
        for r in ranges:
            for i in r:
                df.loc[(month, day), str(i)] = 1
    df["total_asleep"] = df.iloc[:, -60:-1].sum(axis=1)
    return df


def part1(df: pd.DataFrame) -> int:
    sleepiest_guard = (
        df[["guard", "total_asleep"]]
        .groupby("guard")
        .sum()
        .sort_values(by="total_asleep", ascending=False)
        .reset_index()
        .loc[0, "guard"]
    )
    sleepiest_minute = int(
        pd.Series(
            df[df["guard"] == sleepiest_guard]
            .drop(columns=["guard", "total_asleep"])
            .sum(axis=0)
        ).idxmax()
    )
    return sleepiest_guard * sleepiest_minute


def part2(df: pd.DataFrame) -> int:
    sleepy_guards = df.groupby("guard").sum().drop(columns=["total_asleep"])
    max_minute = None
    max_sleeps = -float("inf")
    for m in range(60):
        this_max_sleeps = max(sleepy_guards[str(m)])
        if this_max_sleeps > max_sleeps:
            max_sleeps = this_max_sleeps
            max_minute = m
    # The minute slept most was {m}, with a guard who slept during it {max_sleeps} times
    guard = sleepy_guards[str(max_minute)].idxmax()
    return guard * max_minute


if __name__ == "__main__":
    input = get_data(day=4, year=2018)
    df = assemble_table(input)
    print(f"Part 1 solution: {part1(df)}")
    print(f"Part 2 solution: {part2(df)}")
