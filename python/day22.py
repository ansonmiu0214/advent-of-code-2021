from collections import deque
from dataclasses import dataclass, field
import re
import sys
from typing import Dict, List, NamedTuple

from python.util import run_solution


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int


class CoordinateRange(NamedTuple):
    min_incl: int
    max_incl: int

    def __contains__(self, other: "CoordinateRange") -> bool:
        """..."""

        return self.min_incl <= other.min_incl and other.max_incl <= self.max_incl

    def __len__(self) -> int:
        """..."""

        return self.max_incl - self.min_incl + 1


class RebootStep(NamedTuple):
    on: bool
    x_range: CoordinateRange
    y_range: CoordinateRange
    z_range: CoordinateRange


@dataclass
class CubeSingleDimension:
    ranges: Dict[CoordinateRange, "CubeSingleDimension"] = field(default_factory=dict)

    def insert(self, *ranges: CoordinateRange) -> None:
        """..."""

        if not ranges:
            return

        new_range, *other_new_ranges = ranges

        new_ranges = deque([new_range])

        while new_ranges:
            new_range = new_ranges.popleft()

            overlapping_dimension_ranges = (
                (existing_range, existing_next_dimension)
                for existing_range, existing_next_dimension in self.ranges.items()
                if has_overlap(existing_range, new_range)
            )

            try:
                existing_range, existing_next_dimension = next(
                    overlapping_dimension_ranges
                )
            except StopIteration:
                next_dimension = CubeSingleDimension()
                self.ranges[new_range] = next_dimension
                next_dimension.insert(*other_new_ranges)
                continue

            if existing_range == new_range:
                # existing_range: **********
                # new_range     : **********

                existing_next_dimension.insert(*other_new_ranges)
                continue

            del self.ranges[existing_range]

            if existing_range in new_range:
                # existing_range:    ****
                # new_range     : **********

                if new_range.min_incl < existing_range.min_incl:
                    new_coordinate_range_left = CoordinateRange(
                        min_incl=new_range.min_incl,
                        max_incl=existing_range.min_incl - 1,
                    )

                    # Add the "excess" new range to the queue to be processed
                    # in a later iteration, in case there is an overlapping
                    # coordinate range for this excess.

                    new_ranges.append(new_coordinate_range_left)

                existing_next_dimension.insert(*other_new_ranges)
                self.ranges[existing_range] = existing_next_dimension

                if existing_range.max_incl < new_range.max_incl:
                    new_coordinate_range_right = CoordinateRange(
                        min_incl=existing_range.max_incl + 1,
                        max_incl=new_range.max_incl,
                    )

                    # Add the "excess" new range to the queue to be processed
                    # in a later iteration, in case there is an overlapping
                    # coordinate range for this excess.

                    new_ranges.append(new_coordinate_range_right)

            elif new_range in existing_range:
                # existing_range: **********
                # new_range     :    ****

                if existing_range.min_incl < new_range.min_incl:
                    existing_coordinate_range_left = CoordinateRange(
                        min_incl=existing_range.min_incl,
                        max_incl=new_range.min_incl - 1,
                    )

                    next_dimension = existing_next_dimension.clone()
                    self.ranges[existing_coordinate_range_left] = next_dimension

                next_dimension = existing_next_dimension.clone()
                next_dimension.insert(*other_new_ranges)
                self.ranges[new_range] = next_dimension

                if new_range.max_incl < existing_range.max_incl:
                    existing_coordinate_range_right = CoordinateRange(
                        min_incl=new_range.max_incl + 1,
                        max_incl=existing_range.max_incl,
                    )
                    next_dimension = existing_next_dimension.clone()
                    self.ranges[existing_coordinate_range_right] = next_dimension

            elif existing_range.min_incl < new_range.min_incl:
                # existing_range: *****
                # new_range     :   *****

                existing_coordinate_range_left = CoordinateRange(
                    min_incl=existing_range.min_incl,
                    max_incl=new_range.min_incl - 1,
                )
                next_dimension = existing_next_dimension.clone()
                self.ranges[existing_coordinate_range_left] = next_dimension

                new_coordinate_range_left = CoordinateRange(
                    min_incl=new_range.min_incl, max_incl=existing_range.max_incl
                )
                next_dimension = existing_next_dimension.clone()
                next_dimension.insert(*other_new_ranges)
                self.ranges[new_coordinate_range_left] = next_dimension

                # Add the "excess" new range to the queue to be processed
                # in a later iteration, in case there is an overlapping
                # coordinate range for this excess.

                new_coordinate_range_right = CoordinateRange(
                    min_incl=existing_range.max_incl + 1,
                    max_incl=new_range.max_incl,
                )

                new_ranges.append(new_coordinate_range_right)

            elif new_range.min_incl < existing_range.min_incl:
                # existing_range:   *****
                # new_range     : *****

                new_coordinate_range_left = CoordinateRange(
                    min_incl=new_range.min_incl,
                    max_incl=existing_range.min_incl - 1,
                )

                # Add the "excess" new range to the queue to be processed
                # in a later iteration, in case there is an overlapping
                # coordinate range for this excess.

                new_ranges.append(new_coordinate_range_left)

                existing_coordinate_range_left = CoordinateRange(
                    min_incl=existing_range.min_incl, max_incl=new_range.max_incl
                )
                next_dimension = existing_next_dimension.clone()
                next_dimension.insert(*other_new_ranges)
                self.ranges[existing_coordinate_range_left] = next_dimension

                existing_coordinate_range_right = CoordinateRange(
                    min_incl=new_range.max_incl + 1,
                    max_incl=existing_range.max_incl,
                )
                next_dimension = existing_next_dimension.clone()
                self.ranges[existing_coordinate_range_right] = next_dimension

    def remove(self, *ranges: CoordinateRange):
        """..."""

        if not ranges:
            return True

        range_to_delete, *other_ranges_to_delete = ranges

        if not self.ranges:
            return True

        overlapping_dimension_ranges = [
            (existing_range, existing_next_dimension)
            for existing_range, existing_next_dimension in self.ranges.items()
            if has_overlap(existing_range, range_to_delete)
        ]

        for existing_range, existing_next_dimension in overlapping_dimension_ranges:
            if existing_range in range_to_delete:
                # existing_range :    ****
                # range_to_delete: **********

                if existing_next_dimension.remove(*other_ranges_to_delete):
                    del self.ranges[existing_range]

            elif range_to_delete in existing_range:
                # existing_range : **********
                # range_to_delete:    ****

                del self.ranges[existing_range]

                if existing_range.min_incl < range_to_delete.min_incl:
                    existing_coordinate_range_left = CoordinateRange(
                        min_incl=existing_range.min_incl,
                        max_incl=range_to_delete.min_incl - 1,
                    )

                    next_dimension = existing_next_dimension.clone()
                    self.ranges[existing_coordinate_range_left] = next_dimension

                next_dimension = existing_next_dimension.clone()
                self.ranges[range_to_delete] = next_dimension
                if next_dimension.remove(*other_ranges_to_delete):
                    del self.ranges[range_to_delete]

                if range_to_delete.max_incl < existing_range.max_incl:
                    existing_coordinate_range_right = CoordinateRange(
                        min_incl=range_to_delete.max_incl + 1,
                        max_incl=existing_range.max_incl,
                    )
                    next_dimension = existing_next_dimension.clone()
                    self.ranges[existing_coordinate_range_right] = next_dimension

            elif existing_range.min_incl < range_to_delete.min_incl:
                # existing_range : *****
                # range_to_delete:   *****

                del self.ranges[existing_range]

                existing_coordinate_range_left = CoordinateRange(
                    min_incl=existing_range.min_incl,
                    max_incl=range_to_delete.min_incl - 1,
                )
                next_dimension = existing_next_dimension.clone()
                self.ranges[existing_coordinate_range_left] = next_dimension

                new_coordinate_range_left = CoordinateRange(
                    min_incl=range_to_delete.min_incl, max_incl=existing_range.max_incl
                )
                next_dimension = existing_next_dimension.clone()
                self.ranges[new_coordinate_range_left] = next_dimension
                if next_dimension.remove(*other_ranges_to_delete):
                    del self.ranges[new_coordinate_range_left]

            elif range_to_delete.min_incl < existing_range.min_incl:
                # existing_range :   *****
                # range_to_delete: *****

                del self.ranges[existing_range]

                existing_coordinate_range_left = CoordinateRange(
                    min_incl=existing_range.min_incl, max_incl=range_to_delete.max_incl
                )
                next_dimension = existing_next_dimension.clone()
                self.ranges[existing_coordinate_range_left] = next_dimension
                if next_dimension.remove(*other_ranges_to_delete):
                    del self.ranges[existing_coordinate_range_left]

                existing_coordinate_range_right = CoordinateRange(
                    min_incl=range_to_delete.max_incl + 1,
                    max_incl=existing_range.max_incl,
                )
                next_dimension = existing_next_dimension.clone()
                self.ranges[existing_coordinate_range_right] = next_dimension

        return len(self.ranges) == 0

    def clone(self) -> "CubeSingleDimension":
        """..."""

        return CubeSingleDimension(
            ranges={
                coordinate_range: dimension.clone()
                for coordinate_range, dimension in self.ranges.items()
            }
        )

    def __len__(self) -> int:
        """..."""

        if not self.ranges:
            return 1

        return sum(
            len(coordinate_range) * len(dimension)
            for coordinate_range, dimension in self.ranges.items()
        )


def parse_reboot_step(line: str) -> RebootStep:
    """..."""

    pattern = re.compile(
        r"(?P<state>on|off) x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+),y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+),z=(?P<z_min>-?\d+)..(?P<z_max>-?\d+)"
    )

    match = pattern.match(line)
    assert match is not None, f"Invalid input: {line}"

    parameters = match.groupdict()
    on = parameters["state"] == "on"
    x_min = int(parameters["x_min"])
    x_max = int(parameters["x_max"])
    y_min = int(parameters["y_min"])
    y_max = int(parameters["y_max"])
    z_min = int(parameters["z_min"])
    z_max = int(parameters["z_max"])

    return RebootStep(
        on=on,
        x_range=CoordinateRange(x_min, x_max),
        y_range=CoordinateRange(y_min, y_max),
        z_range=CoordinateRange(z_min, z_max),
    )


def parse_reboot_steps(input: str) -> List[RebootStep]:
    """..."""

    return list(map(parse_reboot_step, input.splitlines()))


def has_overlap(range: CoordinateRange, other_range: CoordinateRange) -> bool:
    """..."""

    return not (
        range.min_incl > other_range.max_incl or range.max_incl < other_range.min_incl
    )


def part1(input: str) -> int:
    """..."""

    reboot_steps = parse_reboot_steps(input)

    cube = CubeSingleDimension()
    valid_area = CoordinateRange(min_incl=-50, max_incl=50)

    for step in reboot_steps:
        if all(
            range in valid_area for range in (step.x_range, step.y_range, step.z_range)
        ):
            if step.on:
                cube.insert(step.x_range, step.y_range, step.z_range)
            else:
                cube.remove(step.x_range, step.y_range, step.z_range)

    return len(cube)


def part2(input: str) -> int:
    """..."""

    reboot_steps = parse_reboot_steps(input)

    cube = CubeSingleDimension()

    for step in reboot_steps:
        if step.on:
            cube.insert(step.x_range, step.y_range, step.z_range)
        else:
            cube.remove(step.x_range, step.y_range, step.z_range)

    return len(cube)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
