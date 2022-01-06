import re
import sys
from typing import Generator, List, NamedTuple, Set, Tuple

from python.util import run_solution


class Point(NamedTuple):
    x: int
    y: int


Vent = Tuple[Point, Point]


def parse_vent(line: str) -> Vent:
    """..."""

    pattern = re.compile("(?P<x1>\d+),(?P<y1>\d+) -> (?P<x2>\d+),(?P<y2>\d+)")

    match = pattern.match(line)
    assert match, f"Cannot recognise line: {line}"

    groupdict = match.groupdict()

    return (
        Point(x=int(groupdict["x1"]), y=int(groupdict["y1"])),
        Point(x=int(groupdict["x2"]), y=int(groupdict["y2"])),
    )


def parse_vents(input: str) -> List[Vent]:
    """..."""

    return list(map(parse_vent, input.splitlines()))


def is_horizontal(start: Point, end: Point) -> bool:
    """..."""

    x1, _ = start
    x2, _ = end

    return x1 == x2


def is_vertical(start: Point, end: Point) -> bool:
    """..."""

    _, y1 = start
    _, y2 = end

    return y1 == y2


def get_points_in_between(start: Point, end: Point) -> Generator[Point, None, None]:
    """..."""

    x1, y1 = start
    x2, y2 = end

    if x1 <= x2:
        xs = range(x1, x2 + 1)
    else:
        xs = range(x1, x2 - 1, -1)

    if y1 <= y2:
        ys = range(y1, y2 + 1)
    else:
        ys = range(y1, y2 - 1, -1)

    if is_vertical(start, end):
        return (Point(x, y1) for x in xs)

    elif is_horizontal(start, end):
        return (Point(x1, y) for y in ys)

    return (Point(x, y) for x, y in zip(xs, ys))


def find_intersections(vents: List[Vent], *, ignore_diagonals: bool) -> Set[Point]:
    """..."""

    seen_points: Set[Point] = set()
    points_with_at_least_two_overlaps: Set[Point] = set()

    for start, end in vents:
        if ignore_diagonals and not (
            is_horizontal(start, end) or is_vertical(start, end)
        ):
            continue

        for point in get_points_in_between(start, end):
            if point not in seen_points:
                seen_points.add(point)
                continue

            if point not in points_with_at_least_two_overlaps:
                points_with_at_least_two_overlaps.add(point)

    return points_with_at_least_two_overlaps


def part1(input: str) -> int:
    """..."""

    vents = parse_vents(input)
    return len(find_intersections(vents, ignore_diagonals=True))


def part2(input: str) -> int:
    """..."""

    vents = parse_vents(input)
    return len(find_intersections(vents, ignore_diagonals=False))


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
