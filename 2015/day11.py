from aocd import get_data
from collections import Counter
from itertools import pairwise

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=11, year=2015)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FORBIDDEN = ("i", "o", "l")


def meets_req1(password: str) -> bool:
    straights = [ALPHABET[i : i + 3] for i in range(len(ALPHABET) - 2)]
    for i, _ in enumerate(password):
        if password[i : i + 3] in straights:
            return True
    return False


def meets_req2(password: str) -> bool:
    return all(char not in password for char in FORBIDDEN)


def meets_req3(password: str) -> bool:
    pairs = Counter(pair for pair in pairwise(password) if pair[0] == pair[1])
    return len(pairs) >= 2


def is_valid(password: str) -> bool:
    return meets_req1(password) and meets_req2(password) and meets_req3(password)


def skip_forbidden_letters(password: str, forbidden=FORBIDDEN) -> str:
    password = [char for char in password]
    skip_to = {"i": "j", "l": "m", "o": "p"}
    for i, char in enumerate(password):
        if char in forbidden:
            a_length = len(password) - i - 1
            next = password[:i] + [skip_to[char]] + (["a"] * a_length)
            return "".join(next)
    return "".join(password)


def increment(password: str) -> str:
    # TODO: redo this, using the other two requirements to logic out what the
    # next valid password must be instead of checking most of them
    password = skip_forbidden_letters(password)
    password = [char for char in password]
    ix = -1
    done = False
    while not done:
        next_char_ix = (ALPHABET.index(password[ix]) + 1) % len(ALPHABET)
        next_char = ALPHABET[next_char_ix]
        password[ix] = next_char
        if next_char == "a":
            ix -= 1
        else:
            done = True
    return "".join(password)


def next_password(password: str) -> str:
    while True:
        password = increment(password)
        if is_valid(password):
            return password


if __name__ == "__main__":
    p1_ans = next_password(input)
    print(f"Part 1 answer: {p1_ans}")
    p2_ans = next_password(p1_ans)
    print(f"Part 2 answer: {p2_ans}")
