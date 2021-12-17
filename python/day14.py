import re
import sys
from typing import Counter, Dict, NamedTuple, Tuple

from python.util import run_solution


PairInsertionRules = Dict[str, str]

class SubmarineManual(NamedTuple):
    polymer_template: str
    pair_insertion_rules: PairInsertionRules


def parse_pair_insertion_rule(line: str) -> Tuple[str, str]:
    """..."""

    pattern = re.compile(r"([A-Z]{2,2}) -> ([A-Z])")

    match = pattern.match(line)
    assert match is not None, f"Invalid line ({line})"

    return match.group(1), match.group(2)


def parse_submarine_manual(input: str) -> SubmarineManual:
    """..."""

    polymer_template, pair_insertion_rules_input = input.split("\n\n")

    pair_insertion_rules_lines = pair_insertion_rules_input.splitlines()
    pair_insertion_rules = dict(
        map(parse_pair_insertion_rule, pair_insertion_rules_lines)
    )

    return SubmarineManual(polymer_template, pair_insertion_rules)


def encode_into_pair_counts(polymer: str) -> Counter[Tuple[str, str]]:
    """..."""

    pairs = list(zip(polymer, polymer[1:]))
    return Counter(pairs)    


def apply_pair_insertion_rules(
    pair_counts: Counter[Tuple[str, str]],
    pair_insertion_rules: PairInsertionRules,
    *,
    num_times: int
) -> Counter[Tuple[str, str]]:
    """..."""

    for _ in range(num_times):
        new_pair_counts = Counter()
    
        for (x, y), count in pair_counts.items():
            new_pair_counts[(x, pair_insertion_rules[f"{x}{y}"])] += count
            new_pair_counts[(pair_insertion_rules[f"{x}{y}"], y)] += count

        pair_counts = new_pair_counts
    
    return pair_counts


def decode_pair_counts_into_element_counts(
    pair_counts: Counter[Tuple[str, str]],
    *,
    first_element: str
) -> Counter[str]:
    """..."""

    element_counts = Counter()
    for (_, y), count in pair_counts.items():
        element_counts[y] += count
    
    element_counts[first_element] += 1
    return element_counts


def part1(input: str) -> int:
    """..."""

    polymer_template, pair_insertion_rules = parse_submarine_manual(input)

    pair_counts = encode_into_pair_counts(polymer_template)

    new_pair_counts = apply_pair_insertion_rules(
        pair_counts,
        pair_insertion_rules,
        num_times=10
    )

    element_counter = decode_pair_counts_into_element_counts(
        new_pair_counts,
        first_element=polymer_template[0]
    )

    frequencies = element_counter.most_common()
    _, most_common_quantity = frequencies[0]
    _, least_common_quantity = frequencies[-1]

    return most_common_quantity - least_common_quantity


def part2(input: str) -> int:
    """..."""

    polymer_template, pair_insertion_rules = parse_submarine_manual(input)

    pair_counts = encode_into_pair_counts(polymer_template)

    new_pair_counts = apply_pair_insertion_rules(
        pair_counts,
        pair_insertion_rules,
        num_times=40
    )

    element_counter = decode_pair_counts_into_element_counts(
        new_pair_counts,
        first_element=polymer_template[0]
    
    )

    frequencies = element_counter.most_common()
    _, most_common_quantity = frequencies[0]
    _, least_common_quantity = frequencies[-1]

    return most_common_quantity - least_common_quantity


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))