import collections
import functools
import re
import sys
from typing import Counter, List, Literal, NamedTuple, Union

from python.util import run_solution


class Dot(NamedTuple):
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class FoldInstruction(NamedTuple):
    axis: Union[Literal["x"], Literal["y"]]
    value: int


class TransparentPaper(NamedTuple):
    grid: Counter[Dot]
    instructions: List[FoldInstruction]


def parse_dot(line: str) -> Dot:
    """..."""

    tokens = line.split(",")
    assert len(tokens) == 2, (
        f"Expected 2 tokens on line '{line}', found {len(tokens)}"
    )

    x, y = tokens
    return Dot(x=int(x), y=int(y))


def parse_grid(input: str) -> Counter[Dot]:
    """..."""

    return collections.Counter(map(parse_dot, input.splitlines()))


def parse_instruction(line: str) -> FoldInstruction:
    """..."""

    pattern = re.compile(r"fold along (?P<axis>[xy])=(?P<value>\d+)")

    match = pattern.match(line)
    assert match is not None, f"Invalid input ({line})"

    return FoldInstruction(axis=match.group("axis"), value=int(match.group("value")))


def parse_transparent_paper(input: str) -> TransparentPaper:
    """..."""

    grid_input, instructions_input = input.split("\n\n")

    grid = parse_grid(grid_input)
    instructions = list(map(parse_instruction, instructions_input.splitlines()))

    return TransparentPaper(grid=grid, instructions=instructions)


def count_visible_dots(grid: Counter[Dot]) -> int:
    """..."""

    return len(grid)


def apply_fold(grid: Counter[Dot], fold: FoldInstruction) -> Counter[Dot]:
    """..."""

    new_grid: Counter[Dot] = collections.Counter()

    for dot, count in grid.items():
        if getattr(dot, fold.axis) < fold.value:
            new_grid[dot] += count
        else:
            distance_to_line = getattr(dot, fold.axis) - fold.value

            new_position = Dot(
                x=dot.x - 2 * distance_to_line if fold.axis == "x" else dot.x,
                y=dot.y - 2 * distance_to_line if fold.axis == "y" else dot.y
            )
            new_grid[new_position] += count

    return new_grid


def visualise_grid(grid: Counter[Dot]) -> None:
    """..."""

    visible_dots = list(grid.keys())

    max_width = max(dot.x for dot in visible_dots)
    max_height = max(dot.y for dot in visible_dots)

    canvas = [["." for _ in range(max_width + 1)] for _ in range(max_height + 1)]

    for col, row in visible_dots:
        canvas[row][col] = "#"
    
    for row in canvas:
        print("".join(row))


def part1(input: str) -> int:
    """..."""

    grid, instructions = parse_transparent_paper(input)

    new_grid = apply_fold(grid, instructions[0])

    return count_visible_dots(new_grid)


def part2(input: str) -> int:
    """..."""

    grid, instructions = parse_transparent_paper(input)

    grid = functools.reduce(
        apply_fold,
        instructions,
        grid
    )
    
    visualise_grid(grid)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))