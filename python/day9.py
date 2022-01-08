import functools
import sys
from collections import deque
from typing import Generator, List, Set, Tuple

from python.util import run_solution


MAX_HEIGHT = 9

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


def adjacent_to(grid: Grid, x: int, y: int) -> Generator[Point, None, None]:
    """..."""

    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return (point for point in neighbors if on_grid(grid, *point))


def find_lowest_points(grid: Grid) -> List[Point]:
    """..."""

    num_rows, num_cols = dimensions(grid)

    return [
        (x, y)
        for x in range(num_rows)
        for y in range(num_cols)
        if all(
            grid[x][y] < grid[adjacent_x][adjacent_y]
            for adjacent_x, adjacent_y in adjacent_to(grid, x, y)
        )
    ]


def find_basin(grid: Grid, root_x: int, root_y: int) -> Set[Point]:
    """..."""

    basin: Set[Point] = set()
    candidates = deque([(root_x, root_y)])

    while candidates:
        x, y = point = candidates.popleft()
        basin.add(point)

        for neighbor in adjacent_to(grid, x, y):
            neighbor_x, neighbor_y = neighbor
            if grid[x][y] < grid[neighbor_x][neighbor_y] < MAX_HEIGHT:
                candidates.append(neighbor)

    return basin


def part1(input: str) -> int:
    """..."""

    grid = parse_grid(input)

    lowest_points = find_lowest_points(grid)
    return sum(grid[x][y] for x, y in lowest_points) + len(lowest_points)


def part2(input: str) -> int:
    """..."""

    grid = parse_grid(input)

    lowest_points = find_lowest_points(grid)
    basin_sizes = sorted(
        (len(find_basin(grid, *point)) for point in lowest_points), reverse=True
    )

    return functools.reduce(lambda x, y: x * y, basin_sizes[:3])


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
