import functools
import sys
from typing import List, NamedTuple, Sequence, Union

from python.util import run_solution


class CorruptLine(NamedTuple):
    first_corrupt_token: str


class IncompleteLine(NamedTuple):
    completion_string: Sequence[str]


class ValidLine(NamedTuple):
    pass


def process_line(line: str) -> Union[CorruptLine, IncompleteLine, ValidLine]:
    """..."""

    opening_to_closing = {"(": ")", "[": "]", "{": "}", "<": ">"}

    stack: List[str] = []
    for char in line:
        if char in opening_to_closing:
            stack.append(char)
            continue

        expected = opening_to_closing[stack.pop()]
        if char != expected:
            return CorruptLine(first_corrupt_token=char)

    if stack:
        return IncompleteLine(
            completion_string=reversed(list(map(opening_to_closing.get, stack)))
        )
    else:
        return ValidLine()


def get_score_for_corrupt_line(line: CorruptLine) -> int:
    """..."""

    score_for_char = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    return score_for_char[line.first_corrupt_token]


def get_score_for_incomplete_line(line: IncompleteLine) -> int:

    score_for_char = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    increments = map(score_for_char.get, line.completion_string)
    return functools.reduce(lambda acc, inc: 5 * acc + inc, increments)


def take_middle(nums: List[int]) -> int:
    """..."""

    sorted_nums = sorted(nums)
    middle_idx = len(nums) // 2

    return sorted_nums[middle_idx]


def part1(input: str) -> int:
    """..."""

    processed_lines = map(process_line, input.splitlines())
    corrupt_lines = filter(lambda line: isinstance(line, CorruptLine), processed_lines)
    return sum(map(get_score_for_corrupt_line, corrupt_lines))


def part2(input: str) -> int:
    """..."""

    processed_lines = map(process_line, input.splitlines())
    incomplete_lines = filter(
        lambda line: isinstance(line, IncompleteLine), processed_lines
    )
    scores_for_incomplete_lines = list(
        map(get_score_for_incomplete_line, incomplete_lines)
    )
    return take_middle(scores_for_incomplete_lines)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
