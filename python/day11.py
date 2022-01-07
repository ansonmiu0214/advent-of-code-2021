import sys
from collections import deque
from typing import Generator, List, Set, Tuple

from python.util import run_solution


MAX_ENERGY_LEVEL = 9

Grid = List[List[int]]
Point = Tuple[int, int]


def parse_grid(input: str) -> Grid:
    """..."""

    return [list(map(int, line)) for line in input.splitlines()]


def dimensions(grid: Grid) -> Tuple[int, int]:
    """..."""

    num_rows = len(grid)
    num_cols = len(grid[0])

    return num_rows, num_cols


def on_grid(grid: Grid, x: int, y: int) -> bool:
    """..."""

    num_rows, num_cols = dimensions(grid)
    return 0 <= x < num_rows and 0 <= y < num_cols


def get_adjacent(grid: Grid, x: int, y: int) -> Generator[Point, None, None]:
    """..."""

    deltas = (-1, 0, 1)
    return (
        (x + delta_x, y + delta_y)
        for delta_x in deltas
        for delta_y in deltas
        if on_grid(grid, x + delta_x, y + delta_y) and not (delta_x == delta_y == 0)
    )


def simulate_timestep(grid: Grid) -> Tuple[Grid, Set[Point]]:
    """..."""

    num_rows, num_cols = dimensions(grid)
    for x in range(num_rows):
        for y in range(num_cols):
            grid[x][y] += 1

    flashed: Set[Point] = set()
    flash_candidates = deque(
        [
            (x, y)
            for x in range(num_rows)
            for y in range(num_cols)
            if grid[x][y] > MAX_ENERGY_LEVEL
        ]
    )

    seen: Set[Point] = set()
    while flash_candidates:
        point = flash_candidates.popleft()
        if point in seen:
            continue

        flashed.add(point)
        seen.add(point)

        x, y = point
        for adjacent in get_adjacent(grid, x, y):
            adjacent_x, adjacent_y = adjacent
            grid[adjacent_x][adjacent_y] += 1

            if grid[adjacent_x][adjacent_y] > 9 and adjacent not in flashed:
                flash_candidates.append(adjacent)

    for x, y in flashed:
        grid[x][y] = 0

    return grid, flashed


def part1(input: str) -> int:
    """..."""

    grid = parse_grid(input)

    total_flashes = 0
    for _ in range(100):
        grid, flashes = simulate_timestep(grid)
        total_flashes += len(flashes)

    return total_flashes


def part2(input: str) -> int:
    """..."""

    grid = parse_grid(input)

    num_rows, num_cols = dimensions(grid)
    total_elems = num_rows * num_cols

    i = 0
    while True:
        grid, flashes = simulate_timestep(grid)

        i += 1
        if len(flashes) == total_elems:
            return i


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
