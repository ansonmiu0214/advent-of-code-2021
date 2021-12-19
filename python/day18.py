import functools
import sys
from typing import NamedTuple, Optional, Tuple, Union

from python.util import run_solution


class SnailfishNumber(NamedTuple):
    first: "Element"
    second: "Element"

    def __str__(self) -> str:
        return f"[{self.first},{self.second}]"


Element = Union[int, SnailfishNumber]


class ExplodeAction(NamedTuple):
    first: int
    second: int


class PropagateAction(NamedTuple):
    first: Optional[int] = None
    second: Optional[int] = None


def _parse_element(line: str, *, start_index: int) -> Tuple[Element, int]:
    """..."""

    end_index = start_index
    if line[end_index] != "[":
        literal = 0

        while line[end_index].isnumeric():
            literal *= 10
            literal += int(line[end_index])
            end_index += 1

        return literal, end_index

    else:
        return _parse_snailfish_number(line, start_index=end_index)


def _parse_snailfish_number(
    line: str, *, start_index: int
) -> Tuple[SnailfishNumber, int]:
    """..."""

    end_index = start_index
    assert (
        line[end_index] == "["
    ), f"Expected '[' on index {end_index}, got {line[end_index]}"
    end_index += 1

    first, end_index = _parse_element(line, start_index=end_index)
    assert (
        line[end_index] == ","
    ), f"Expected ',' on index {end_index}, got {line[end_index]}"
    end_index += 1

    second, end_index = _parse_element(line, start_index=end_index)
    assert (
        line[end_index] == "]"
    ), f"Expected ']' on index {end_index}, got {line[end_index]}"
    end_index += 1

    return SnailfishNumber(first, second), end_index


def parse_snailfish_number(line: str) -> SnailfishNumber:
    """..."""

    snailfish_number, end_index = _parse_snailfish_number(line, start_index=0)
    assert end_index == len(line), f"Unprocessed tokens: {line[end_index:]}"

    return snailfish_number


def add_snailfish_numbers(
    lhs: SnailfishNumber, rhs: SnailfishNumber
) -> SnailfishNumber:
    """..."""

    return SnailfishNumber(lhs, rhs)


def pair_only_has_regular_numbers(num: SnailfishNumber) -> bool:
    """..."""

    return type(num.first) is int and type(num.second) is int


def propagate_to_leftmost(elem: Element, *, value: int):
    """..."""

    if type(elem) is int:
        return elem + value

    first = propagate_to_leftmost(elem.first, value=value)
    return SnailfishNumber(first, elem.second)


def propagate_to_rightmost(elem: Element, *, value: int):
    """..."""

    if type(elem) is int:
        return elem + value

    second = propagate_to_rightmost(elem.second, value=value)
    return SnailfishNumber(elem.first, second)


def apply_explode_action_if_applicable(
    num: SnailfishNumber, *, level: int
) -> Tuple[Union[ExplodeAction, PropagateAction, None], SnailfishNumber]:
    """..."""

    if pair_only_has_regular_numbers(num):
        if level >= 4:
            return ExplodeAction(num.first, num.second), num
        else:
            return None, num

    if type(num.first) is SnailfishNumber:
        action_from_first, first = apply_explode_action_if_applicable(
            num.first, level=level + 1
        )

        if action_from_first is not None:

            if type(action_from_first) is ExplodeAction:
                first = 0
                second = propagate_to_leftmost(
                    num.second, value=action_from_first.second
                )

            elif type(action_from_first) is PropagateAction:
                if action_from_first.second is not None:
                    second = propagate_to_leftmost(
                        num.second, value=action_from_first.second
                    )
                else:
                    second = num.second

            return PropagateAction(
                first=action_from_first.first, second=None
            ), SnailfishNumber(first, second)

    else:
        first = num.first

    if type(num.second) is SnailfishNumber:
        action_from_second, second = apply_explode_action_if_applicable(
            num.second, level=level + 1
        )

        if action_from_second is not None:

            if type(action_from_second) is ExplodeAction:
                first = propagate_to_rightmost(
                    num.first, value=action_from_second.first
                )
                second = 0

            elif type(action_from_second) is PropagateAction:
                if action_from_second.first is not None:
                    first = propagate_to_rightmost(
                        num.first, value=action_from_second.first
                    )
                else:
                    first = num.first

            return PropagateAction(
                first=None, second=action_from_second.second
            ), SnailfishNumber(first, second)
    else:
        second = num.second

    return None, SnailfishNumber(first, second)


def apply_split_action_if_applicable(num: Element) -> Tuple[bool, Element]:
    """..."""

    if type(num) is int:
        if num >= 10:
            half, remainder = divmod(num, 2)
            new_element = SnailfishNumber(half, half + remainder)
            return True, new_element
        else:
            return False, num

    first_had_split, new_first = apply_split_action_if_applicable(num.first)
    if first_had_split:
        return True, SnailfishNumber(new_first, num.second)

    second_had_split, new_second = apply_split_action_if_applicable(num.second)
    if second_had_split:
        return True, SnailfishNumber(num.first, new_second)

    return False, num


def reduce_snailfish_number(num: SnailfishNumber) -> SnailfishNumber:
    """..."""

    try_explode, num = apply_explode_action_if_applicable(num, level=0)
    if try_explode is not None:
        return reduce_snailfish_number(num)

    try_split, num = apply_split_action_if_applicable(num)
    if try_split:
        return reduce_snailfish_number(num)

    return num


def add_snailfish_numbers_in_reduced_form(
    lhs: SnailfishNumber, rhs: SnailfishNumber
) -> SnailfishNumber:
    """..."""

    sum = add_snailfish_numbers(lhs, rhs)
    return reduce_snailfish_number(sum)


def magnitude(elem: Element) -> int:
    """..."""

    if type(elem) is int:
        return elem

    return 3 * magnitude(elem.first) + 2 * magnitude(elem.second)


def part1(input: str) -> int:
    """..."""

    snailfish_numbers = map(parse_snailfish_number, input.splitlines())

    sum_of_snailfish_numbers = functools.reduce(
        add_snailfish_numbers_in_reduced_form, snailfish_numbers
    )

    return magnitude(sum_of_snailfish_numbers)


def part2(input: str) -> int:
    """..."""

    snailfish_numbers = list(map(parse_snailfish_number, input.splitlines()))

    possible_pairs_of_snailfish_numbers = [
        (lhs, rhs)
        for x, lhs in enumerate(snailfish_numbers)
        for y, rhs in enumerate(snailfish_numbers)
        if x != y
    ]

    return max(
        magnitude(add_snailfish_numbers_in_reduced_form(lhs, rhs))
        for lhs, rhs in possible_pairs_of_snailfish_numbers
    )


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
