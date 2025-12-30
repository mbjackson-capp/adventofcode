from aocd import get_data
from typing import Tuple

# set session token first - https://github.com/wimglenn/advent-of-code-wim/issues/1

input = get_data(day=9, year=2017)

SKIPPED = "_"


def clean_post_exclams(stream: str) -> str:
    """Create a new version of the stream, canceling out characters immediately
    after an exclamation point as described in problem text."""
    new_stream = ""
    skip_ahead = False
    am_inside_garbage = False
    for _, char in enumerate(stream):
        if skip_ahead:
            new_stream += SKIPPED
            skip_ahead = False
            continue

        if char == "!":
            skip_ahead = True

        if char == "<" and not am_inside_garbage:
            am_inside_garbage = True

        if char == ">":
            am_inside_garbage = False

        new_stream += char
    return new_stream


def remove_garbage(stream: str) -> Tuple[str, int]:
    """Remove all garbage from the stream and count how many non-trivial garbage
    characters are between brackets without being canceled or doing canceling."""
    new_stream = ""
    n_canceled = 0
    am_inside_garbage = False
    for _, char in enumerate(stream):
        if char == ">":
            am_inside_garbage = False
            continue

        if char == "<" and not am_inside_garbage:
            am_inside_garbage = True
            continue

        if not am_inside_garbage:
            new_stream += char
        else:
            if not char in ("!", SKIPPED):
                n_canceled += 1
    return new_stream, n_canceled


def clean_stream_score(stream: str) -> int:
    """Linear time non-recursive method that infers what 'depth' of nesting
    would be from simple counting."""
    depth = 0
    score = 0
    for char in stream:
        if char == "{":
            depth += 1
        elif char == "}":
            score += depth
            depth -= 1
    assert depth == 0, f"Depth should be 0 at end of stream, instead it's {depth}"
    return score


def solve(stream: str):
    declammed = clean_post_exclams(stream)
    degarbaged, p2_ans = remove_garbage(declammed)
    score = clean_stream_score(degarbaged)
    return score, p2_ans


if __name__ == "__main__":
    p1_ans, p2_ans = solve(input)
    print(f"Part 1 answer: {p1_ans}")
    print(f"Part 2 answer: {p2_ans}")
