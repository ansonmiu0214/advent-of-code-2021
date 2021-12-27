import sys
from typing import List, Tuple

from python.util import run_solution


Seafloor = List[List[str]]


EAST_FACING = ">"
SOUTH_FACING = "v"
VACANT = "."


def parse_seafloor(input: str) -> Seafloor:
    """..."""

    return [list(line) for line in input.splitlines()]


def dimensions(seafloor: Seafloor) -> Tuple[int, int]:
    """..."""

    num_rows, num_cols = len(seafloor), len(seafloor[0])
    return num_rows, num_cols


def next_step(x: int, y: int, *, seafloor: Seafloor) -> Tuple[int, int]:
    """..."""

    num_rows, num_cols = dimensions(seafloor)

    if seafloor[x][y] == EAST_FACING:
        new_location = (x, 0 if (y + 1) == num_cols else (y + 1))
    elif seafloor[x][y] == SOUTH_FACING:
        new_location = (0 if (x + 1) == num_rows else (x + 1), y)
    else:
        raise ValueError(f"No sea cucumber found at ({x},{y}): {seafloor[x][y]}")

    return new_location


def try_move_sea_cucumbers(seafloor: Seafloor, *, herd: str) -> Tuple[Seafloor, bool]:
    """..."""

    num_rows, num_cols = dimensions(seafloor)

    relevant_sea_cucumbers = (
        ((x, y), next_step(x, y, seafloor=seafloor))
        for x in range(num_rows)
        for y in range(num_cols)
        if seafloor[x][y] == herd
    )

    moveable_relevant_facing_sea_cucumbers = [
        ((x, y), (new_x, new_y))
        for (x, y), (new_x, new_y) in relevant_sea_cucumbers
        if seafloor[new_x][new_y] == VACANT
    ]

    if not moveable_relevant_facing_sea_cucumbers:
        return seafloor, False

    new_seafloor = [[seafloor[x][y] for y in range(num_cols)] for x in range(num_rows)]

    for (old_x, old_y), (new_x, new_y) in moveable_relevant_facing_sea_cucumbers:
        new_seafloor[new_x][new_y], new_seafloor[old_x][old_y] = (
            new_seafloor[old_x][old_y],
            new_seafloor[new_x][new_y],
        )

    return new_seafloor, True


def try_perform_step(seafloor: Seafloor):
    """..."""

    seafloor, east_herd_has_moved = try_move_sea_cucumbers(seafloor, herd=EAST_FACING)
    seafloor, south_herd_has_moved = try_move_sea_cucumbers(seafloor, herd=SOUTH_FACING)

    has_moved = east_herd_has_moved or south_herd_has_moved

    return seafloor, has_moved


def part1(input: str) -> int:
    """..."""

    seafloor = parse_seafloor(input)

    has_changed = True
    num_steps = 0
    while has_changed:
        seafloor, has_changed = try_perform_step(seafloor)
        num_steps += 1

    return num_steps


def part2(input: str) -> int:
    """..."""

    print("Nothing to do :) Merry Christmas!")
    return 2022


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
