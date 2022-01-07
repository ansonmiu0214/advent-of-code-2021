import sys
from typing import Callable, List

from python.util import run_solution


def parse_crabs(input: str) -> List[int]:
    """..."""

    return list(map(int, input.split(",")))


def uniform_fuel(positions: List[int], common_pos: int) -> int:
    """..."""

    return sum(abs(position - common_pos) for position in positions)


def triangle_number(x: int) -> int:
    """..."""

    return x * (x + 1) // 2


def linear_fuel(positions: List[int], common_pos: int) -> int:
    """..."""

    steps = (abs(position - common_pos) for position in positions)
    weighted_steps = (triangle_number(step) for step in steps)
    return sum(weighted_steps)


def find_common_position_with_cheapest_fuel(
    positions: List[int], *, fuel_metric: Callable[[List[int], int], int]
) -> int:
    """Return the common position, in the specified 'positions', that all crabs
    can move to with the cheapest total fuel, computed using the specified
    'fuel_metric'. The 'fuel_metric' returns the total fuel required to move
    all crabs in the existing 'positions' to a particular position."""

    min_position = min(positions)
    max_position = max(positions)

    return min(
        fuel_metric(positions, pos) for pos in range(min_position, max_position + 1)
    )


def part1(input: str) -> int:
    """..."""

    crabs = parse_crabs(input)
    return find_common_position_with_cheapest_fuel(crabs, fuel_metric=uniform_fuel)


def part2(input: str) -> int:
    """..."""

    crabs = parse_crabs(input)
    return find_common_position_with_cheapest_fuel(crabs, fuel_metric=linear_fuel)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
