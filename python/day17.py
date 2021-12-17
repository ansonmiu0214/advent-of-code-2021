import functools
import multiprocessing
import os
import re
import sys
from typing import List, NamedTuple, Optional

from python.util import run_solution


class TargetArea(NamedTuple):
    x_min: int
    x_max: int
    y_min: int
    y_max: int


class XY(NamedTuple):
    x: int
    y: int


class State(NamedTuple):
    position: XY
    velocity: XY


Trajectory = List[State]


def parse_target_area(line: str) -> TargetArea:
    """..."""

    pattern = re.compile(
        r"target area: x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+), y=(?P<y_min>-?\d+)..(?P<y_max>-?\d+)"
    )

    match = pattern.match(line)
    assert match is not None, f"Invalid input: {line}"

    target_area_parameters = {
        key: int(val)
        for key, val in match.groupdict().items()
    }

    return TargetArea(**target_area_parameters)


def in_target_area(target_area: TargetArea, position: XY) -> bool:
    """..."""

    x, y = position

    return target_area.x_min <= x <= target_area.x_max \
        and target_area.y_min <= y <= target_area.y_max


def simulate_step(state: State) -> State:
    """..."""

    next_position = XY(
        x=state.position.x + state.velocity.x,
        y=state.position.y + state.velocity.y,
    )

    x_velocity = state.velocity.x + (
        0 if state.velocity.x == 0 else
        -1 if state.velocity.x > 0 else
        1
    )

    y_velocity = state.velocity.y - 1

    return State(position=next_position, velocity=XY(x_velocity, y_velocity))


def find_maximum_height(states: Trajectory) -> int:
    """..."""

    return max(state.position.y for state in states)


def overshot(position: XY, target_area: TargetArea) -> bool:
    """..."""

    return position.x > target_area.x_max or position.y < target_area.y_min


def simulate_trajectory(
    initial_velocity: XY,
    *,
    initial_position: XY,
    target_area: TargetArea
) -> Optional[Trajectory]:
    """..."""

    state = State(position=initial_position, velocity=initial_velocity)
    trajectory = [state]

    while not overshot(state.position, target_area):
        state = simulate_step(state)
        trajectory.append(state)

        if in_target_area(target_area, state.position):
            return trajectory

    return None


def find_plausible_trajectories_for_any_initial_velocity(
    target_area: TargetArea
) -> List[Trajectory]:
    """..."""
    
    origin = XY(0, 0)
    candidate_initial_velocities = (
        XY(x, y)
        for x in range(1, target_area.x_max + 1)
        for y in range(-abs(target_area.y_min), abs(target_area.y_min) + 1)
    )

    simulate_trajectory_given_initial_velocity = functools.partial(
        simulate_trajectory,
        initial_position=origin,
        target_area=target_area
    )
    
    with multiprocessing.Pool(os.cpu_count() or 4) as pool:
        trajectories = pool.map(simulate_trajectory_given_initial_velocity, candidate_initial_velocities)

    return list(filter(None, trajectories))


def part1(input: str) -> int:
    """..."""

    target_area = parse_target_area(input)

    trajectories = find_plausible_trajectories_for_any_initial_velocity(target_area)
    return max(map(find_maximum_height, trajectories))


def part2(input: str) -> int:
    """..."""

    target_area = parse_target_area(input)

    trajectories = find_plausible_trajectories_for_any_initial_velocity(target_area)
    return len(trajectories)

if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))