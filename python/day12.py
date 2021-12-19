import collections
import sys
from typing import Callable, Counter, Dict, List, Set, Tuple

from python.util import run_solution


Cave = str
Path = List[Cave]
Passage = Tuple[Cave, Cave]
Layout = Dict[Cave, Set[Cave]]
CaveVisitStrategy = Callable[[Cave, Counter[Cave]], bool]


def parse_passage(line: str) -> Passage:
    """..."""

    passage = line.split("-")
    assert (
        len(passage) == 2
    ), f"Expected 2 tokens on line '{line}', found {len(passage)}"

    return passage


def parse_layout(input: str) -> Layout:
    """..."""

    layout: Layout = collections.defaultdict(set)

    for line in input.splitlines():
        cave1, cave2 = parse_passage(line)
        layout[cave1].add(cave2)
        layout[cave2].add(cave1)

    return layout


def is_start(cave: str) -> bool:
    """..."""

    return cave == "start"


def is_end(cave: str) -> bool:
    """..."""

    return cave == "end"


def is_terminal(cave: str) -> bool:
    """..."""

    return is_start(cave) or is_end(cave)


def is_big_cave(cave: str) -> bool:
    """..."""

    return not is_terminal(cave) and all(letter.isupper() for letter in cave)


def is_small_cave(cave: str) -> bool:
    """..."""

    return not is_terminal(cave) and all(letter.islower() for letter in cave)


def find_paths(
    layout: Layout,
    path_so_far: Path,
    curr_cave: Cave,
    *,
    visit_count: Counter[Cave],
    can_visit_cave: CaveVisitStrategy,
) -> None:
    """..."""

    all_paths: List[Path] = []

    if not can_visit_cave(curr_cave, visit_count):
        return all_paths

    visit_count[curr_cave] += 1
    path_so_far.append(curr_cave)

    if is_end(curr_cave):
        all_paths.append(list(path_so_far))
    else:
        for neighbour in layout[curr_cave]:
            all_paths += find_paths(
                layout,
                path_so_far=path_so_far,
                curr_cave=neighbour,
                visit_count=visit_count,
                can_visit_cave=can_visit_cave,
            )

    path_so_far.pop()
    visit_count[curr_cave] -= 1

    return all_paths


def part1(input: str) -> int:
    """..."""

    def can_visit_cave(cave: Cave, prev_visit_counts: Counter[Cave]) -> bool:
        """..."""

        if prev_visit_counts[cave] == 0:
            return True

        if is_start(cave) or is_small_cave(cave):
            return False

        return True

    layout = parse_layout(input)
    paths = find_paths(
        layout,
        path_so_far=[],
        curr_cave="start",
        visit_count=collections.Counter(),
        can_visit_cave=can_visit_cave,
    )
    return len(paths)


def part2(input: str) -> int:
    """..."""

    def can_visit_cave(cave: Cave, prev_visit_counts: Counter[Cave]) -> bool:
        """..."""

        if prev_visit_counts[cave] == 0:
            return True

        if is_start(cave):
            return False

        if is_small_cave(cave):
            if prev_visit_counts[cave] > 1:
                return False

            if any(
                visit_count > 1
                for existing_cave, visit_count in prev_visit_counts.items()
                if is_small_cave(existing_cave) and existing_cave != cave
            ):
                return False

        return True

    layout = parse_layout(input)
    paths = find_paths(
        layout,
        path_so_far=[],
        curr_cave="start",
        visit_count=collections.Counter(),
        can_visit_cave=can_visit_cave,
    )

    return len(paths)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
