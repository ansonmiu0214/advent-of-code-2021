from collections import deque
from dataclasses import dataclass
import math
import sys
from typing import Dict, List, NamedTuple, Set, Tuple

from python.util import run_solution


@dataclass(frozen=True, order=True)
class Coordinate:
    x: int
    y: int

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        """..."""

        return Coordinate(x=self.x - other.x, y=self.y - other.y)

    def __len__(self) -> int:
        """..."""

        return abs(self.x) + abs(self.y)

    def __iter__(self):
        """..."""

        yield self.x
        yield self.y


class Sideroom(NamedTuple):
    expected_amphipod: str
    coordinates: List[Coordinate]


Grid = List[List[str]]


class Diagram(NamedTuple):
    grid: Grid
    hallway: List[Coordinate]
    siderooms: Dict[str, Sideroom]


class Amphipod(NamedTuple):
    name: str
    coordinate: Coordinate


WALL = "#"
OUTSIDE = " "
VACANT = "."

ENERGY_PER_STEP = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def parse_grid(input: str) -> Grid:
    """..."""

    grid = [list(line) for line in input.splitlines()]

    row_length = max(len(row) for row in grid)
    for row in grid:
        if len(row) < row_length:
            row += list(" " * (row_length - len(row)))

    return grid


def dimensions(grid: List[List[str]]) -> Tuple[int, int]:
    """..."""

    num_rows = len(grid)
    num_cols = len(grid[0])

    return num_rows, num_cols


def parse_siderooms(grid: Grid, *, size: int) -> Dict[str, Sideroom]:
    """..."""

    num_rows, num_cols = dimensions(grid)

    siderooms_coordinates = [
        [Coordinate(x + i, y) for i in range(size)]
        for x in range(num_rows - 1)
        for y in range(num_cols)
        if all(grid[x + i][y].isalpha() for i in range(size))
    ]

    assert (
        len(siderooms_coordinates) == 4
    ), f"Expected 4 siderooms, found {len(siderooms_coordinates)}"

    sideroom_amphipods = "ABCD"

    return {
        amphipod: Sideroom(
            expected_amphipod=amphipod,
            coordinates=sorted(coordinates, reverse=True),
        )
        for amphipod, coordinates in zip(sideroom_amphipods, siderooms_coordinates)
    }


def parse_diagram(input: str, *, sideroom_size: int) -> Diagram:
    """..."""

    grid = parse_grid(input)
    num_rows, num_cols = dimensions(grid)

    siderooms = parse_siderooms(grid, size=sideroom_size)
    hallway = [
        Coordinate(x, y)
        for x in range(num_rows)
        for y in range(num_cols)
        if grid[x][y] == VACANT
    ]

    return Diagram(grid=grid, hallway=hallway, siderooms=siderooms)


def on_grid(point: Coordinate, *, grid: Grid) -> bool:
    """..."""

    num_rows, num_cols = dimensions(grid)

    x, y = point
    return 0 <= x < num_rows and 0 <= y < num_cols


def is_organised(diagram: Diagram) -> bool:
    """..."""

    return all(
        all(diagram.grid[x][y] == expected_amphipod for x, y in sideroom.coordinates)
        for expected_amphipod, sideroom in diagram.siderooms.items()
    )


def is_amphipod(cell: str, *, diagram: Diagram) -> bool:
    """..."""

    return cell in diagram.siderooms


def amphipod_is_organised(amphipod: Amphipod, *, diagram: Diagram) -> bool:
    """..."""

    return any(
        amphipod.coordinate == coordinate
        for coordinate in diagram.siderooms[amphipod.name]
    )


def adjacent(coordinate: Coordinate):
    """..."""

    x, y = coordinate

    yield Coordinate(x - 1, y)
    yield Coordinate(x + 1, y)
    yield Coordinate(x, y - 1)
    yield Coordinate(x, y + 1)


def is_accessible(point: Coordinate, *, grid: Grid) -> bool:
    """..."""

    x, y = point
    return grid[x][y] == VACANT


def reachable(current: Coordinate, *, diagram: Diagram) -> List[Coordinate]:
    """..."""

    grid = diagram.grid

    reachable_coordinates: Set[Coordinate] = set()
    candidates = deque([current])

    while candidates:
        point = candidates.popleft()
        reachable_coordinates.add(point)

        for neighbor in adjacent(point):
            if all(
                [
                    on_grid(neighbor, grid=grid),
                    is_accessible(neighbor, grid=grid),
                    neighbor not in reachable_coordinates,
                ]
            ):
                candidates.append(neighbor)

    # Filter out current coordinate.

    reachable_coordinates.remove(current)

    # Sort in ascending order of distance from current

    return sorted(
        (
            reachable_coordinate
            for reachable_coordinate in reachable_coordinates
            if reachable_coordinate.x != current.x
            and reachable_coordinate.y != current.y
        ),
        key=lambda coordinate: len(coordinate - current),
    )


def next_diagram(diagram: Diagram, *, start: Coordinate, end: Coordinate) -> Diagram:
    """..."""

    num_rows, num_cols = dimensions(diagram.grid)

    grid = [[diagram.grid[x][y] for y in range(num_cols)] for x in range(num_rows)]

    # Move 'start' to 'end', essentially performing a swap.

    grid[start.x][start.y], grid[end.x][end.y] = (
        grid[end.x][end.y],
        grid[start.x][start.y],
    )

    return Diagram(grid=grid, hallway=diagram.hallway, siderooms=diagram.siderooms)


def serialise_grid(grid: Grid) -> str:
    """..."""

    return "\n".join("".join(row) for row in grid)


def organise_amphipods(
    diagram: Diagram,
    cache: Dict[str, int] = dict(),
    seen_grids: Set[str] = set(),
):
    """..."""

    acc = math.inf

    grid = diagram.grid
    serialised_grid = serialise_grid(grid)

    if is_organised(diagram):
        return 0

    if serialised_grid in seen_grids:
        return acc

    if serialised_grid in cache:
        return cache[serialised_grid]

    seen_grids.add(serialised_grid)

    num_rows, num_cols = dimensions(grid)

    amphipods = [
        Amphipod(name=grid[x][y], coordinate=Coordinate(x, y))
        for x in range(num_rows)
        for y in range(num_cols)
        if is_amphipod(grid[x][y], diagram=diagram)
    ]

    # For each amphipod in the hallway:
    #: o if its allocated sideroom has vacancies:
    #:   o move into the bottom-most vacant slot in that sideroom, such that any
    #:     slots below that slot already contain the correct amphipod.

    hallway_amphipods = [
        amphipod for amphipod in amphipods if amphipod.coordinate in diagram.hallway
    ]

    for hallway_amphipod in hallway_amphipods:
        reachable_spots = reachable(hallway_amphipod.coordinate, diagram=diagram)
        matching_sideroom = diagram.siderooms[hallway_amphipod.name]

        for idx, sideroom_slot in enumerate(matching_sideroom.coordinates):
            if sideroom_slot not in reachable_spots:
                continue

            if not all(
                grid[sideroom_slot_below.x][sideroom_slot_below.y]
                == hallway_amphipod.name
                for sideroom_slot_below in matching_sideroom.coordinates[:idx]
            ):
                continue

            acc = min(
                acc,
                organise_amphipods(
                    next_diagram(
                        diagram,
                        start=hallway_amphipod.coordinate,
                        end=sideroom_slot,
                    ),
                    cache=cache,
                    seen_grids=seen_grids,
                )
                + (
                    len(hallway_amphipod.coordinate - sideroom_slot)
                    * ENERGY_PER_STEP[hallway_amphipod.name]
                ),
            )

    num_slots_per_sideroom = min(
        len(sideroom.coordinates) for sideroom in diagram.siderooms.values()
    )

    # For each sideroom with a slot that contains an incorrect amphipod, try
    # move the incorrect amphipod to each vacant slot in the hallway.  If the
    # incorrect amphipod is blocked by some other amphipod, move the blocker to
    # each vacant slot in the hallway.

    for expected_amphipod, sideroom in diagram.siderooms.items():
        for slot_idx in range(num_slots_per_sideroom - 1, -1, -1):
            slot_coordinate = sideroom.coordinates[slot_idx]
            if is_accessible(slot_coordinate, grid=grid):
                continue

            if all(
                grid[slot_below.x][slot_below.y] == expected_amphipod
                for slot_below in sideroom.coordinates[: slot_idx + 1]
            ):
                continue

            if not all(
                is_accessible(slot_above, grid=grid)
                for slot_above in sideroom.coordinates[slot_idx + 1 :]
            ):
                continue

            amphipod = grid[slot_coordinate.x][slot_coordinate.y]
            for reachable_spot in reachable(slot_coordinate, diagram=diagram):
                if reachable_spot in diagram.hallway and not any(
                    reachable_spot.y == coordinate.y
                    for sideroom in diagram.siderooms.values()
                    for coordinate in sideroom.coordinates
                ):
                    acc = min(
                        acc,
                        organise_amphipods(
                            next_diagram(
                                diagram,
                                start=slot_coordinate,
                                end=reachable_spot,
                            ),
                            cache=cache,
                            seen_grids=seen_grids,
                        )
                        + (
                            len(slot_coordinate - reachable_spot)
                            * ENERGY_PER_STEP[amphipod]
                        ),
                    )

    seen_grids.remove(serialised_grid)
    cache[serialised_grid] = acc

    return acc


def print_grid(grid: List[List[str]]) -> None:
    """..."""

    for row in grid:
        print("".join(row))


def part1(input: str) -> int:
    """..."""

    diagram = parse_diagram(input, sideroom_size=2)

    minimum_energy_to_reorganise = organise_amphipods(diagram)
    return minimum_energy_to_reorganise


def unfold_diagram(input: str) -> str:
    """..."""

    lines = input.splitlines()
    missing_lines = [
        "  #D#C#B#A#",
        "  #D#B#A#C#",
    ]

    return "\n".join([*lines[:3], *missing_lines, *lines[3:]])


def part2(input: str) -> int:
    """..."""

    unfolded_input = unfold_diagram(input)
    diagram = parse_diagram(unfolded_input, sideroom_size=4)

    minimum_energy_to_reorganise = organise_amphipods(diagram)
    return minimum_energy_to_reorganise


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
