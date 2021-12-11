import functools
import sys
from typing import Callable, Dict, List, Literal, NamedTuple, TypeVar, Union

from python.util import run_solution


_SUPPORTED_COMMANDS = ("forward", "down", "up")


class Command(NamedTuple):
    direction: Union[Literal["forward"], Literal["down"], Literal["up"]]
    magnitude: int


def parse_command(line: str) -> Command:
    """..."""

    tokens = line.split(" ")
    assert len(tokens) == 2, (
        f"Expected 2 tokens on line '{line}', found {len(tokens)}"
    )

    direction = tokens[0]
    assert direction in _SUPPORTED_COMMANDS, (
        f"Direction '{direction}' not one of the supported: "
        f"{','.join(_SUPPORTED_COMMANDS)}"
    )

    magnitude = int(tokens[1])
    return Command(direction, magnitude)


def parse_commands(input: str) -> List[Command]:
    """..."""

    return map(parse_command, input.splitlines())


State = TypeVar("State")


def simulate_commands(
    commands: List[Command],
    transitions: Dict[str, Callable[[Command, State], State]],
    initialState: State
) -> State:
    """..."""

    return functools.reduce(
        lambda state, command: transitions[command.direction](command, state),
        commands,
        initialState
    )


def part1(input: str) -> int:
    """..."""

    commands = parse_commands(input)

    class State(NamedTuple):
        horizontal_position: int
        depth: int

    StateTransition = Callable[[Command, State], State]

    forward: StateTransition = lambda command, state: State(
        horizontal_position=state.horizontal_position + command.magnitude,
        depth=state.depth
    )

    down: StateTransition = lambda command, state: State(
        horizontal_position=state.horizontal_position,
        depth=state.depth + command.magnitude
    )

    up: StateTransition = lambda command, state: State(
        horizontal_position=state.horizontal_position,
        depth=state.depth - command.magnitude
    )

    transitions = dict(forward=forward, down=down, up=up)

    initial_state = State(horizontal_position=0, depth=0)
    final_state = simulate_commands(commands, transitions, initial_state)

    return final_state.horizontal_position * final_state.depth


def part2(input: str) -> int:
    """..."""

    commands = parse_commands(input)

    class State(NamedTuple):
        horizontal_position: int
        depth: int
        aim: int

    StateTransition = Callable[[Command, State], State]

    forward: StateTransition = lambda command, state: State(
        horizontal_position=state.horizontal_position + command.magnitude,
        depth=state.depth + state.aim * command.magnitude,
        aim=state.aim
    )

    down: StateTransition = lambda command, state: State(
        horizontal_position=state.horizontal_position,
        depth=state.depth,
        aim=state.aim + command.magnitude
    )

    up: StateTransition = lambda command, state: State(
        horizontal_position=state.horizontal_position,
        depth=state.depth,
        aim=state.aim - command.magnitude
    )

    transitions = dict(forward=forward, down=down, up=up)

    initial_state = State(horizontal_position=0, depth=0, aim=0)
    final_state = simulate_commands(commands, transitions, initial_state)

    return final_state.horizontal_position * final_state.depth


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))