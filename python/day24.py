from enum import Enum, auto
import re
import sys
from typing import Dict, List, NamedTuple

from python.util import run_solution


class InstructionGroup(NamedTuple):
    divisor: int
    check: int
    offset: int


class StackEntry(NamedTuple):
    input_idx: int
    offset: int


class Constraint(NamedTuple):
    input_idx: int
    top_of_stack_input_idx: int
    offset: int


class OptimisationStrategy(Enum):
    MAXIMISE = auto()
    MINIMISE = auto()


def parse_instruction_group(match: re.Match) -> InstructionGroup:
    """..."""

    divisor = match.group("divisor")
    check = match.group("check")
    offset = match.group("offset")

    return InstructionGroup(divisor=int(divisor), check=int(check), offset=int(offset))


def parse_instruction_groups(input: str) -> List[InstructionGroup]:
    """..."""

    pattern = re.compile(
        r"""inp w
mul x 0
add x z
mod x 26
div z (?P<divisor>1|26)
add x (?P<check>-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (?P<offset>-?\d+)
mul y x
add z y"""
    )

    return list(map(parse_instruction_group, re.finditer(pattern, input)))


def generate_constraints(instructions: List[InstructionGroup]) -> List[Constraint]:
    """..."""

    stack: List[StackEntry] = []
    constraints: List[Constraint] = []

    for input_idx, instruction in enumerate(instructions):
        if instruction.divisor == 1:
            # Push
            stack.append(StackEntry(input_idx=input_idx, offset=instruction.offset))

        else:
            # Pop, such that 'w[input_idx] == stack[-1]'
            top_of_stack_entry = stack.pop()
            constraints.append(
                Constraint(
                    input_idx=input_idx,
                    top_of_stack_input_idx=top_of_stack_entry.input_idx,
                    offset=top_of_stack_entry.offset + instruction.check,
                )
            )

    assert not stack, "Unable to generate constraints from instructions"

    return constraints


def generate_optimal_value(
    constraint: Constraint, *, allowed_digits: List[int], strategy: OptimisationStrategy
):
    """..."""

    candidates = [
        (val, val + constraint.offset)
        for val in allowed_digits
        if val + constraint.offset in allowed_digits
    ]

    if strategy == OptimisationStrategy.MAXIMISE:
        optimal_candidate = max(candidates)
    else:
        optimal_candidate = min(candidates)

    more_significant, less_significant = optimal_candidate
    return {
        constraint.top_of_stack_input_idx: more_significant,
        constraint.input_idx: less_significant,
    }


def generate_optimal_value_from_constraints(
    constraints: List[Constraint],
    *,
    allowed_digits: List[int],
    strategy: OptimisationStrategy
):
    """..."""

    optimal_values: Dict[int, int] = {}
    for constraint in constraints:
        optimal_values.update(
            generate_optimal_value(
                constraint, allowed_digits=allowed_digits, strategy=strategy
            )
        )

    optimal_digits = [None for _ in range(len(optimal_values))]
    for idx, value in optimal_values.items():
        optimal_digits[idx] = value

    return int("".join(map(str, optimal_digits)))


def part1(input: str) -> int:
    """..."""

    instruction_groups = parse_instruction_groups(input)

    constraints = generate_constraints(instruction_groups)

    return generate_optimal_value_from_constraints(
        constraints,
        allowed_digits=list(range(1, 10)),
        strategy=OptimisationStrategy.MAXIMISE,
    )


def part2(input: str) -> int:
    """..."""

    instruction_groups = parse_instruction_groups(input)

    constraints = generate_constraints(instruction_groups)

    return generate_optimal_value_from_constraints(
        constraints,
        allowed_digits=list(range(1, 10)),
        strategy=OptimisationStrategy.MINIMISE,
    )


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
