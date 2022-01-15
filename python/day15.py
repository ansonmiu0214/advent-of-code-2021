import sys
from typing import Dict, List, Tuple

from python.util import run_solution


Cavern = List[List[int]]
Position = Tuple[int, int]


def parse_cavern(input: str) -> Cavern:
    """..."""

    return [list(map(int, line)) for line in input.splitlines()]


def get_dimensions(cavern: Cavern) -> Tuple[int, int]:
    """..."""

    vertical = len(cavern)
    horizontal = len(cavern[0])

    return vertical, horizontal


def in_bounds(cavern: Cavern, position: Position) -> bool:
    """..."""

    x, y = position
    num_rows, num_cols = get_dimensions(cavern)

    return 0 <= x < num_rows and 0 <= y < num_cols


def get_adjacents(position: Position) -> List[Position]:
    """..."""

    x, y = position
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def find_minimum_risk_from_top_left_to_bottom_right(cavern: Cavern) -> int:
    """..."""

    num_rows, num_cols = get_dimensions(cavern)
    bottom_right = (num_rows - 1, num_cols - 1)

    candidates: Dict[Position, int] = {(0, 0): 0}
    seen = set()

    while candidates:
        min_risk, curr_position = min(
            (risk, position) for position, risk in candidates.items()
        )
        del candidates[curr_position]
        seen.add(curr_position)

        if curr_position == bottom_right:
            return min_risk

        for adjacent_position in get_adjacents(curr_position):
            if not in_bounds(cavern, adjacent_position):
                continue

            if adjacent_position in seen:
                continue

            x, y = adjacent_position
            if adjacent_position in candidates:
                candidates[adjacent_position] = min(
                    candidates[adjacent_position], min_risk + cavern[x][y]
                )
            else:
                candidates[adjacent_position] = min_risk + cavern[x][y]


def increment(cavern: Cavern) -> Cavern:
    """..."""

    return [[1 if risk == 9 else risk + 1 for risk in row] for row in cavern]


def render_full_map(cavern: Cavern, *, scale: int) -> Cavern:
    """..."""

    sections = [[None for _ in range(scale)] for _ in range(scale)]
    sections[0][0] = cavern

    for row in range(scale):
        for col in range(scale):
            if row == col == 0:
                continue

            if row == 0:
                sections[row][col] = increment(sections[row][col - 1])
            else:
                sections[row][col] = increment(sections[row - 1][col])

    num_rows, num_cols = get_dimensions(cavern)
    full_num_rows = num_rows * scale
    full_num_cols = num_cols * scale

    full_map = [[None for _ in range(full_num_cols)] for _ in range(full_num_rows)]

    for section_row_idx, section_row in enumerate(sections):
        for section_col_idx, chunk in enumerate(section_row):

            full_row_offset = section_row_idx * num_rows
            full_col_offset = section_col_idx * num_cols

            for row_idx, row in enumerate(chunk):
                for col_idx, risk in enumerate(row):
                    full_map[full_row_offset + row_idx][
                        full_col_offset + col_idx
                    ] = risk

    return full_map


def part1(input: str) -> int:
    """..."""

    cavern = parse_cavern(input)

    return find_minimum_risk_from_top_left_to_bottom_right(cavern)


def part2(input: str) -> int:
    """..."""

    cavern = parse_cavern(input)
    full_map = render_full_map(cavern, scale=5)

    return find_minimum_risk_from_top_left_to_bottom_right(full_map)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
