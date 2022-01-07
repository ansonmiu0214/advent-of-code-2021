import functools
import sys
from typing import List

from python.util import run_solution


Timer = int


def parse_timers(line: str) -> List[Timer]:
    """..."""

    return list(map(int, line.split(",")))


@functools.lru_cache(maxsize=None)
def fish_count(initial_timer: int, *, num_days: int) -> int:
    """Return the number of fish spawned, over the specified 'num_days', by a
    single fish with the specified 'initial_timer'."""

    if initial_timer >= num_days:
        return 1

    # We decrement 'num_days - initial_timer' by an additional 1 day, because
    # that day was spent at the '0' timer state.

    count_from_original = fish_count(6, num_days=num_days - initial_timer - 1)
    count_from_spawned = fish_count(8, num_days=num_days - initial_timer - 1)

    return count_from_original + count_from_spawned


def simulate(timers: List[int], *, num_days: int) -> int:
    """..."""

    return sum(fish_count(timer, num_days=num_days) for timer in timers)


def part1(input: str) -> int:
    """..."""

    timers = parse_timers(input)
    return simulate(timers, num_days=18)


def part2(input: str) -> int:
    """..."""

    timers = parse_timers(input)
    return simulate(timers, num_days=256)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
