import argparse
import sys
from pathlib import Path
from typing import Callable, List, Literal, Protocol, Union


class CommandLineArgs(Protocol):
    part: Union[Literal[1], Literal[2]]
    input: Path


def parse_args(args: List[str]) -> CommandLineArgs:
    """..."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, choices=[1,2], required=True)
    parser.add_argument("--input", type=Path, required=True)

    return parser.parse_args(args)


def run_solution(
    *,
    part1: Callable[[str], int],
    part2: Callable[[str], int]
) -> int:
    """..."""

    parsed_args = parse_args(sys.argv[1:])

    input = parsed_args.input.read_text()
    solution = part1 if parsed_args.part == 1 else part2
    answer = solution(input)

    print(f"Part {parsed_args.part}: {answer}")
    return 0