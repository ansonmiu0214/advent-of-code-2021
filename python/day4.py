import sys
from typing import List, Tuple

from python.util import run_solution


Board = List[List[int]]


def parse_board(input: str) -> Board:
    """..."""

    board: Board = []
    for line in input.splitlines():
        entries = list(map(int, filter(None, line.split(" "))))
        board.append(entries)
    return board


def parse_input(input: str) -> Tuple[List[int], Board]:

    numbers_line, *boards_input = input.split("\n\n")

    numbers = list(map(int, numbers_line.split(",")))
    boards = list(map(parse_board, boards_input))

    return numbers, boards


def board_has_bingo(board: Board) -> bool:
    """..."""

    return any(all(entry is None for entry in line) for line in board) or any(
        all(line[idx] is None for line in board) for idx in range(len(board))
    )


def apply_number_to_board(number: int, board: Board) -> Board:
    """..."""

    return [[entry if entry != number else None for entry in line] for line in board]


def sum_of_unchecked(board: Board) -> int:
    """..."""

    return sum(entry for line in board for entry in line if entry is not None)


def part1(input: str) -> int:
    """..."""

    numbers, boards = parse_input(input)

    for number in numbers:
        boards = [apply_number_to_board(number, board) for board in boards]
        for board in boards:
            if board_has_bingo(board):
                return number * sum_of_unchecked(board)


def part2(input: str) -> int:
    """..."""

    numbers, boards = parse_input(input)

    board_idxs = set(range(len(boards)))

    for number in numbers:
        boards = [apply_number_to_board(number, board) for board in boards]
        for idx, board in enumerate(boards):
            if idx not in board_idxs:
                continue

            if board_has_bingo(board):
                board_idxs.remove(idx)
                if not board_idxs:
                    return number * sum_of_unchecked(board)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
