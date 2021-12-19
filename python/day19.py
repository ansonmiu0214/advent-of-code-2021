from collections import defaultdict
from dataclasses import dataclass
import functools
import multiprocessing
import os
import re
import sys
from typing import (
    DefaultDict,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Set,
    Tuple,
)

from python.util import run_solution


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __add__(self, other: "Point") -> "Point":
        """..."""

        assert (
            type(other) is Point
        ), f"Expected call argument of type 'Point', got type '{type(other)}'"

        return Point(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other: "Point") -> "Point":
        """..."""

        assert (
            type(other) is Point
        ), f"Expected call argument of type 'Point', got type '{type(other)}'"

        return Point(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __iter__(self) -> Generator[int, None, None]:
        """..."""

        yield self.x
        yield self.y
        yield self.z

    def __str__(self) -> str:
        """..."""

        return f"({self.x},{self.y},{self.z})"

    def __len__(self) -> int:
        """..."""

        return sum(map(abs, [self.x, self.y, self.z]))


@dataclass(eq=True, frozen=True)
class RotationMatrix:
    basis_x: Point
    basis_y: Point
    basis_z: Point

    def __call__(self, other: Point) -> Point:
        """..."""

        assert (
            type(other) is Point
        ), f"Expected call argument of type 'Point', got type '{type(other)}'"

        lhs_x = [getattr(basis, "x") for basis in self]
        lhs_y = [getattr(basis, "y") for basis in self]
        lhs_z = [getattr(basis, "z") for basis in self]

        x = sum(m * n for m, n in zip(lhs_x, other))
        y = sum(m * n for m, n in zip(lhs_y, other))
        z = sum(m * n for m, n in zip(lhs_z, other))

        return Point(x, y, z)

    def __iter__(self) -> Generator[Point, None, None]:
        """..."""

        yield self.basis_x
        yield self.basis_y
        yield self.basis_z


class VectorOperation(Protocol):
    def __call__(self, other: Point) -> Point:
        """..."""


@dataclass
class MultiplyByMatrix(VectorOperation):
    matrix: RotationMatrix

    def __call__(self, other: Point) -> Point:
        return self.matrix(other)


@dataclass
class AddVector(VectorOperation):
    vector: Point

    def __call__(self, other: Point) -> Point:
        return self.vector + other


@dataclass
class Sequential(VectorOperation):
    operations: List[VectorOperation]

    def __call__(self, other: Point) -> Point:
        return functools.reduce(
            lambda vec, operation: operation(vec), self.operations, other
        )


class Scanner(NamedTuple):
    id: int
    beacons: Set[Point]


class AlignmentTransformation(NamedTuple):
    base_scanner_id: int
    relative_scanner_id: int
    normalised_beacons: Set[Point]
    rotation_matrix: RotationMatrix
    translation_vector: Point


ROTATION_MATRICES = [
    # reference orientation
    RotationMatrix(
        Point(1, 0, 0),
        Point(0, 1, 0),
        Point(0, 0, 1),
    ),
    # 90 degrees about y-axis
    RotationMatrix(
        Point(0, 0, -1),
        Point(0, 1, 0),
        Point(1, 0, 0),
    ),
    # 180 degrees about y-axis
    RotationMatrix(
        Point(-1, 0, 0),
        Point(0, 1, 0),
        Point(0, 0, -1),
    ),
    # 270 degrees about y-axis
    RotationMatrix(
        Point(0, 0, 1),
        Point(0, 1, 0),
        Point(-1, 0, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, 1, 0),
        Point(-1, 0, 0),
        Point(0, 0, 1),
    ),
    # ...
    RotationMatrix(
        Point(0, 1, 0),
        Point(0, 0, 1),
        Point(1, 0, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, 1, 0),
        Point(1, 0, 0),
        Point(0, 0, -1),
    ),
    # ...
    RotationMatrix(
        Point(0, 1, 0),
        Point(0, 0, -1),
        Point(-1, 0, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, -1, 0),
        Point(1, 0, 0),
        Point(0, 0, 1),
    ),
    # ...
    RotationMatrix(
        Point(0, -1, 0),
        Point(0, 0, -1),
        Point(1, 0, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, -1, 0),
        Point(-1, 0, 0),
        Point(0, 0, -1),
    ),
    # ...
    RotationMatrix(
        Point(0, -1, 0),
        Point(0, 0, 1),
        Point(-1, 0, 0),
    ),
    # ...
    RotationMatrix(
        Point(1, 0, 0),
        Point(0, 0, 1),
        Point(0, -1, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, 0, -1),
        Point(1, 0, 0),
        Point(0, -1, 0),
    ),
    # ...
    RotationMatrix(
        Point(-1, 0, 0),
        Point(0, 0, -1),
        Point(0, -1, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, 0, 1),
        Point(-1, 0, 0),
        Point(0, -1, 0),
    ),
    # ...
    RotationMatrix(
        Point(1, 0, 0),
        Point(0, -1, 0),
        Point(0, 0, -1),
    ),
    # ...
    RotationMatrix(
        Point(0, 0, -1),
        Point(0, -1, 0),
        Point(-1, 0, 0),
    ),
    # ...
    RotationMatrix(
        Point(-1, 0, 0),
        Point(0, -1, 0),
        Point(0, 0, 1),
    ),
    # ...
    RotationMatrix(
        Point(0, 0, 1),
        Point(0, -1, 0),
        Point(1, 0, 0),
    ),
    # ...
    RotationMatrix(
        Point(1, 0, 0),
        Point(0, 0, -1),
        Point(0, 1, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, 0, -1),
        Point(-1, 0, 0),
        Point(0, 1, 0),
    ),
    # ...
    RotationMatrix(
        Point(-1, 0, 0),
        Point(0, 0, 1),
        Point(0, 1, 0),
    ),
    # ...
    RotationMatrix(
        Point(0, 0, 1),
        Point(1, 0, 0),
        Point(0, 1, 0),
    ),
]


def parse_beacon(line: str) -> Point:
    """..."""

    tokens = list(map(int, line.split(",")))
    assert len(tokens) == 3, f"Expected 3 tokens in line '{line}', got {len(tokens)}"

    x, y, z = tokens
    return Point(x, y, z)


def parse_scanner(lines: str) -> Scanner:
    """..."""

    lines_iter = iter(lines.splitlines())

    header_pattern = re.compile(r"--- scanner (\d+) ---")
    header = next(lines_iter)
    header_match = header_pattern.match(header)

    assert header_match is not None, f"Invalid header: {header}"
    scanner_id = int(header_match.group(1))

    beacons_relative_pos = set(map(parse_beacon, lines_iter))

    return Scanner(scanner_id, beacons_relative_pos)


def try_align_beacons_via_translation(beacons1: Set[Point], beacons2: Set[Point]):
    """..."""

    translation_vector_candidates = (
        beacon1 - beacon2 for beacon1 in beacons1 for beacon2 in beacons2
    )

    for translation_vector in translation_vector_candidates:
        normalised_beacons2 = set(beacon + translation_vector for beacon in beacons2)
        aligned_beacons = beacons1 & normalised_beacons2
        if len(aligned_beacons) >= 12:
            return translation_vector

    return None


def try_align_scanners(
    scanner_pair: Tuple[Scanner, Scanner]
) -> Optional[VectorOperation]:
    """..."""

    base_scanner, relative_scanner = scanner_pair

    for rotation_matrix in ROTATION_MATRICES:
        rotated_beacons2 = set(
            rotation_matrix(beacon) for beacon in relative_scanner.beacons
        )
        translation_vector = try_align_beacons_via_translation(
            base_scanner.beacons, rotated_beacons2
        )
        if translation_vector is not None:
            transform = Sequential(
                [
                    MultiplyByMatrix(rotation_matrix),
                    AddVector(translation_vector),
                ]
            )

            return base_scanner.id, relative_scanner.id, transform

    return None


def find_scanner_alignment_chain(
    relative_to_base_ids: Dict[int, List[int]],
    *,
    goal: int,
    path: List[int],
):
    """..."""

    if path[-1] == goal:
        return True, path

    for base_id in relative_to_base_ids[path[-1]]:
        if base_id not in path:
            path.append(base_id)

            found, path = find_scanner_alignment_chain(
                relative_to_base_ids, goal=goal, path=path
            )
            if found:
                return found, path

            path.pop()

    return False, path


def normalise_transformations(
    alignment_transformations: Dict[int, Dict[int, VectorOperation]],
    scanner_id: int,
    *,
    base_scanner_id: int,
) -> VectorOperation:
    """..."""

    if scanner_id == base_scanner_id:
        return Sequential([])

    path_to_base_scanner_id = [scanner_id]
    assert find_scanner_alignment_chain(
        alignment_transformations, goal=base_scanner_id, path=path_to_base_scanner_id
    )

    steps = zip(path_to_base_scanner_id, path_to_base_scanner_id[1:])
    return Sequential(
        [alignment_transformations[relative][base] for relative, base in steps]
    )


def get_normalised_transforms(scanners: List[Scanner], *, base_scanner_id: int):
    """..."""

    all_scanner_pairs = (
        (base_scanner, relative_scanner)
        for base_scanner in scanners
        for relative_scanner in scanners
        if base_scanner.id != relative_scanner.id
    )

    with multiprocessing.Pool(os.cpu_count() or 4) as pool:
        potential_alignments = filter(
            None, pool.map(try_align_scanners, all_scanner_pairs)
        )

    alignment_transformations: DefaultDict[
        int, Dict[int, VectorOperation]
    ] = defaultdict(dict)

    for base_id, relative_id, transform in potential_alignments:
        alignment_transformations[relative_id][base_id] = transform

    return [
        normalise_transformations(
            alignment_transformations, scanner.id, base_scanner_id=base_scanner_id
        )
        for scanner in scanners
    ]


def part1(input: str) -> int:
    """..."""

    scanners_input = input.split("\n\n")
    scanners = sorted(
        map(parse_scanner, scanners_input), key=lambda scanner: scanner.id
    )

    transforms = get_normalised_transforms(scanners, base_scanner_id=0)

    unique_beacons: Set[Point] = set()
    for scanner, transform in zip(scanners, transforms):
        normalised_beacons = set(map(transform, scanner.beacons))
        unique_beacons |= normalised_beacons

    return len(unique_beacons)


def part2(input: str) -> int:
    """..."""

    scanners_input = input.split("\n\n")
    scanners = sorted(
        map(parse_scanner, scanners_input), key=lambda scanner: scanner.id
    )

    transforms = get_normalised_transforms(scanners, base_scanner_id=0)
    normalised_origins = [transform(Point(0, 0, 0)) for transform in transforms]

    return max(
        len(origin1 - origin2)
        for origin1 in normalised_origins
        for origin2 in normalised_origins
    )


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
