import sys
from collections import deque
from typing import List

from python.util import run_solution


def parse_measurements(input: str) -> List[int]:
    """..."""

    return map(int, input.splitlines())


def count_increments(measurements: List[int], *, window_size: int) -> int:
    """..."""

    assert window_size > 0, f"Window size ({window_size}) must be positive"

    window = deque()
    for index in range(window_size):
        try:
            window.append(next(measurements))
        except StopIteration:
            assert False, (
                f"Window size ({window_size}) must not exceed number of "
                f" measurements ({index + 1})"
            )

    prev_window_sum = sum(window)

    increments = 0
    for curr_measurement in measurements:
        curr_window_sum = prev_window_sum - window.popleft() + curr_measurement
    
        if prev_window_sum < curr_window_sum:
            increments += 1

        window.append(curr_measurement)
        prev_window_sum = curr_window_sum

    return increments


def part1(input: str) -> int:
    """..."""

    measurements = parse_measurements(input)
    return count_increments(measurements, window_size=1)


def part2(input: str) -> int:
    """..."""

    measurements = parse_measurements(input)
    return count_increments(measurements, window_size=3)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))