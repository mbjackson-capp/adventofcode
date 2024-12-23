from aocd import get_data
from math import floor


PRUNE_MODULUS = 16777216


def evolve(secret_num: int) -> int:
    prod64_result = secret_num * 64
    secret_num = prod64_result ^ secret_num
    secret_num %= PRUNE_MODULUS

    div_result = floor(secret_num / 32)
    secret_num = div_result ^ secret_num
    secret_num %= PRUNE_MODULUS

    prod2048_result = secret_num * 2048
    secret_num = prod2048_result ^ secret_num
    secret_num %= PRUNE_MODULUS

    return secret_num


def secret_numbers(secret_num: int, n=2000, part=1) -> int | list[int]:
    results = [secret_num]
    for _ in range(n):
        secret_num = evolve(secret_num)
        results.append(secret_num)
    if part == 1:
        return results[-1]
    return results


def part1(nums: list[int], n=2000) -> int:
    total = 0
    for num in nums:
        secret_num_2000 = secret_numbers(num)
        total += secret_num_2000
    return total


def prices_from(secret_nums: list[int]):
    """Turn the list of secret numbers into a list of single-digit prices."""
    return [i % 10 for i in secret_nums]


def changes_from(prices: list[int]):
    """Turn a list of prices into a list of changes from one price to the next."""
    changes = []
    for ix, price in enumerate(prices):
        if ix == 0:
            changes.append(None)
        else:
            changes.append(price - prices[ix - 1])
    return changes


def execute_sale_strategy(prices: list[int], change_seq: tuple[int]) -> int | None:
    """Iterate through a list of prices to determine how many bananas you would
    earn by making a transaction at the first instance of a provided sequence of
    four changes. Returns None if the sequence is never found and thus no
    transaction occurs."""
    for ix in range(1, len(prices) - 3):
        if (
            prices[ix] - prices[ix - 1] == change_seq[0]
            and prices[ix + 1] - prices[ix] == change_seq[1]
            and prices[ix + 2] - prices[ix + 1] == change_seq[2]
            and prices[ix + 3] - prices[ix + 2] == change_seq[3]
        ):
            return prices[ix + 3]


def get_all_change_seqs(initial_nums: list[int]) -> list[int]:
    """Obtain all sequences of four changes that actually occur for a list of
    initial monkey numbers. There are about 41,000 of them, which cuts
    down the total runtime to about one-third of what it'd be if evaluating
    all possible sequences of four numbers from -9 to 9."""
    all_prices = []
    all_changes = []
    seqs = set()
    for _, init_num in enumerate(initial_nums):
        prices = prices_from(secret_numbers(init_num, part=2))
        all_prices.append(prices)
        changes = changes_from(prices)
        all_changes.append(changes)
        for ix in range(1, len(changes) - 3):
            seq = tuple(changes[ix : ix + 4])
            seqs.add(seq)
    return seqs, all_prices, all_changes


def try_change_seq(all_price_lists: list[list[int]], change_seq: tuple[int]) -> int:
    """Count the total number of bananas obtained from all monkeys if the same
    sequence of four changes is tested against every monkey's list of prices."""
    total = 0
    for price_list in all_price_lists:
        result = execute_sale_strategy(price_list, change_seq)
        if result is not None:
            total += result
    return total


def part2(input: list[int]) -> int:
    """Determine the highest number of bananas it is possible to get when price list
    for all monkeys in input is compared against the same sequence of four changes.
    Takes about one second per ten sequences generated, i.e. about 4100 seconds or
    1.2 hours.
    TODO: Find a much faster method with less naive iteration."""
    print(f"Generating all sequences of changes...")
    seqs, all_prices, _ = get_all_change_seqs(input)
    print(f"There are {len(seqs)} total sequences to check")
    max_possible_bananas = 0
    for i, change_seq in enumerate(seqs):
        this_banana_total = try_change_seq(all_prices, change_seq)
        if this_banana_total > max_possible_bananas:
            print(f"{this_banana_total} higher than prior max {max_possible_bananas}")
            max_possible_bananas = this_banana_total
        if i % 10 == 0:
            print(f"After {i} sequences evaluated, max is {max_possible_bananas}")
    return max_possible_bananas


if __name__ == "__main__":
    input = [int(i) for i in get_data(day=22, year=2024).split("\n")]
    part1_solution = part1(input)
    print(f"Part 1 solution: {part1_solution}")

    print(f"Now running Part 2. This could take over an hour...")
    part2_solution = part2(input)
    print(f"Part 2 solution: {part2_solution}")
