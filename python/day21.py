from dataclasses import dataclass
import collections
import re
import sys
from typing import Callable, Counter, Dict, Generator, NamedTuple, Tuple

from python.util import run_solution


class Player(NamedTuple):
    id: int
    starting_position: int


class PlayerState(NamedTuple):
    player: Player
    position: int
    score: int


class DeterministicGameResult(NamedTuple):
    winner: PlayerState
    loser: PlayerState
    num_dice_rolls: int


@dataclass
class QuantumGameOutcomes:
    player1_wins: int
    player2_wins: int


def parse_starting_position(line: str) -> Player:
    """..."""

    pattern = re.compile(
        r"Player (?P<id>\d+) starting position: (?P<starting_position>\d+)"
    )
    match = pattern.match(line)
    assert match is not None, f"Invalid input: {line}"

    return Player(
        id=int(match.group("id")),
        starting_position=int(match.group("starting_position")),
    )


def parse_starting_positions(input: str) -> Tuple[Player, Player]:
    """..."""

    lines = input.splitlines()
    assert len(lines) == 2, f"Expected 2 players, got {len(lines)}"

    return tuple(map(parse_starting_position, lines))


def make_deterministic_dice(*, num_sides: int) -> Generator[int, None, None]:
    """..."""

    next_number = 1
    while True:
        yield next_number
        next_number += 1
        if next_number > num_sides:
            next_number = 1


def alternate_players(player1: Player, player2: Player) -> Callable[[Player], Player]:
    """..."""

    def next_player(*, current_player: Player) -> Player:
        """..."""

        return player2 if current_player == player1 else player1

    return next_player


def game_over(
    player1_state: PlayerState, player2_state: PlayerState, *, target_score: int
) -> bool:
    """..."""

    return player1_state.score >= target_score or player2_state.score >= target_score


def update_player_state(
    player_state: PlayerState, steps_to_move: int, *, num_spaces_on_board: int
) -> PlayerState:
    """..."""

    position = player_state.position + steps_to_move
    if position % num_spaces_on_board == 0:
        position = num_spaces_on_board
    else:
        position %= num_spaces_on_board

    score = player_state.score + position

    return PlayerState(player=player_state.player, position=position, score=score)


def simulate_game_with_deterministic_dice(
    player1: Player,
    player2: Player,
    *,
    dice_rolls_per_turn: int = 3,
    num_sides_on_dice: int = 100,
    num_spaces_on_board: int = 10,
    target_score: int = 1000,
) -> DeterministicGameResult:
    """..."""

    player1_state = PlayerState(
        player=player1, position=player1.starting_position, score=0
    )

    player2_state = PlayerState(
        player=player2, position=player2.starting_position, score=0
    )

    num_turns = 0
    dice = make_deterministic_dice(num_sides=num_sides_on_dice)
    current_player = player1
    get_next_player = alternate_players(player1, player2)

    while not game_over(player1_state, player2_state, target_score=target_score):
        steps_to_move = sum(next(dice) for _ in range(dice_rolls_per_turn))

        if current_player == player1:
            player1_state = update_player_state(
                player1_state, steps_to_move, num_spaces_on_board=num_spaces_on_board
            )
        else:
            player2_state = update_player_state(
                player2_state, steps_to_move, num_spaces_on_board=num_spaces_on_board
            )

        num_turns += 1
        current_player = get_next_player(current_player=current_player)

    if player1_state.score >= target_score:
        winner, loser = player1_state, player2_state
    else:
        winner, loser = player2_state, player1_state

    return DeterministicGameResult(
        winner=winner, loser=loser, num_dice_rolls=num_turns * dice_rolls_per_turn
    )


def quantum_dice_outcomes(*, num_sides: int) -> Counter[int]:
    """..."""

    outcomes = (
        dice_1 + dice_2 + dice_3
        for dice_1 in range(1, num_sides + 1)
        for dice_2 in range(1, num_sides + 1)
        for dice_3 in range(1, num_sides + 1)
    )

    return collections.Counter(outcomes)


def explore_game_outcomes_with_quantum_dice(
    player1: Player,
    player2: Player,
    *,
    num_sides_on_dice: int,
    num_spaces_on_board: int,
    target_score: int,
) -> QuantumGameOutcomes:
    """..."""

    quantum_dice_sums = quantum_dice_outcomes(num_sides=num_sides_on_dice)
    next_player = alternate_players(player1, player2)

    outcomes: Dict[Tuple[PlayerState, PlayerState, Player], QuantumGameOutcomes] = {}

    # Base case: if player 1 has a score >= 'target_score' and player 2 has a
    # score < 'target_score', player 1 always wins that game, irrespective of both
    # players' positions and whose turn it is.

    for player1_score in range(target_score, target_score + num_spaces_on_board + 1):
        for player2_score in range(target_score):
            for player1_position in range(1, num_spaces_on_board + 1):
                for player2_position in range(1, num_spaces_on_board + 1):
                    player1_state = PlayerState(
                        player=player1, position=player1_position, score=player1_score
                    )
                    player2_state = PlayerState(
                        player=player2, position=player2_position, score=player2_score
                    )

                    outcomes[
                        (player1_state, player2_state, player1)
                    ] = QuantumGameOutcomes(player1_wins=1, player2_wins=0)
                    outcomes[
                        (player1_state, player2_state, player2)
                    ] = QuantumGameOutcomes(player1_wins=1, player2_wins=0)

    # Base case: if player 2 has a score >= 'target_score' and player 1 has a
    # score < 'target_score', player 2 always wins that game, irrespective of both
    # players' positions and whose turn it is.

    for player2_score in range(target_score, target_score + num_spaces_on_board + 1):
        for player1_score in range(target_score):
            for player2_position in range(1, num_spaces_on_board + 1):
                for player1_position in range(1, num_spaces_on_board + 1):
                    player1_state = PlayerState(
                        player=player1, position=player1_position, score=player1_score
                    )
                    player2_state = PlayerState(
                        player=player2, position=player2_position, score=player2_score
                    )

                    outcomes[
                        (player1_state, player2_state, player1)
                    ] = QuantumGameOutcomes(player1_wins=0, player2_wins=1)
                    outcomes[
                        (player1_state, player2_state, player2)
                    ] = QuantumGameOutcomes(player1_wins=0, player2_wins=1)

    # Recursive case: when both players' scores are < 'target_score'.  Compute
    # the game outcomes in *reverse* order of player scores, because the base case
    # is established at the end game, and we are building the solution bottom-up.

    for player1_score in range(target_score - 1, -1, -1):
        for player2_score in range(target_score - 1, -1, -1):
            for player1_position in range(1, num_spaces_on_board + 1):
                for player2_position in range(1, num_spaces_on_board + 1):
                    player1_state = PlayerState(
                        player1, position=player1_position, score=player1_score
                    )
                    player2_state = PlayerState(
                        player2, position=player2_position, score=player2_score
                    )

                    for curr_player in (player1, player2):
                        scenario = (player1_state, player2_state, curr_player)
                        scenario_outcome = QuantumGameOutcomes(
                            player1_wins=0, player2_wins=0
                        )

                        # 'quantum_dice_sums' specify a mapping from each possible
                        # 'dice_sum' universe to the 'count' of times the universe occurs.
                        # This means that, for each possible 'dice_sum' universe, the next
                        # scenario in that universe occurs 'count' times.

                        for dice_sum, count in quantum_dice_sums.items():
                            if curr_player == player1:
                                next_player_state = update_player_state(
                                    player1_state,
                                    dice_sum,
                                    num_spaces_on_board=num_spaces_on_board,
                                )
                                next_scenario = (
                                    next_player_state,
                                    player2_state,
                                    next_player(current_player=curr_player),
                                )
                            else:
                                next_player_state = update_player_state(
                                    player2_state,
                                    dice_sum,
                                    num_spaces_on_board=num_spaces_on_board,
                                )
                                next_scenario = (
                                    player1_state,
                                    next_player_state,
                                    next_player(current_player=curr_player),
                                )
                            outcomes_from_next_turn = outcomes[next_scenario]

                            scenario_outcome.player1_wins += (
                                outcomes_from_next_turn.player1_wins * count
                            )
                            scenario_outcome.player2_wins += (
                                outcomes_from_next_turn.player2_wins * count
                            )

                        outcomes[scenario] = scenario_outcome

    player1_initial_state = PlayerState(
        player=player1, position=player1.starting_position, score=0
    )
    player2_initial_state = PlayerState(
        player=player2, position=player2.starting_position, score=0
    )

    return outcomes[(player1_initial_state, player2_initial_state, player1)]


def part1(input: str) -> int:
    """..."""

    player1, player2 = parse_starting_positions(input)

    game_result = simulate_game_with_deterministic_dice(
        player1,
        player2,
        dice_rolls_per_turn=3,
        num_sides_on_dice=100,
        num_spaces_on_board=10,
        target_score=1000,
    )

    return game_result.loser.score * game_result.num_dice_rolls


def part2(input: str) -> int:
    """..."""

    player1, player2 = parse_starting_positions(input)

    outcomes = explore_game_outcomes_with_quantum_dice(
        player1, player2, num_sides_on_dice=3, num_spaces_on_board=10, target_score=21
    )

    return max(outcomes.player1_wins, outcomes.player2_wins)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
