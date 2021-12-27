from enum import Enum, auto
import sys
from typing import Counter, List, Optional

from python.util import run_solution


DiagnosticReport = List[List[str]]


class FilterCriterion(Enum):
    MOST_COMMON = auto()
    LEAST_COMMON = auto()


def parse_diagnostic_report(input: str) -> DiagnosticReport:
    """..."""

    return [list(line) for line in input.splitlines()]


def aggregate_bits(
    diagnostic_report: DiagnosticReport, *, criterion: FilterCriterion
) -> str:
    """..."""

    bits = []
    num_bits = len(diagnostic_report[0])

    for bit_idx in range(num_bits):
        bit_counter = Counter(line[bit_idx] for line in diagnostic_report)
        [(most_common_bit, _), (least_common_bit, _)] = bit_counter.most_common()
        if criterion == FilterCriterion.MOST_COMMON:
            bits.append(most_common_bit)
        else:
            bits.append(least_common_bit)

    return "".join(bits)


def bits_to_decimal(bits: str) -> int:
    """..."""

    return int(bits, 2)


def compute_power_consumption(diagnostic_report: DiagnosticReport) -> int:
    """..."""

    gamma_rate = aggregate_bits(
        diagnostic_report, criterion=FilterCriterion.MOST_COMMON
    )
    epsilon_rate = aggregate_bits(
        diagnostic_report, criterion=FilterCriterion.LEAST_COMMON
    )

    return bits_to_decimal(gamma_rate) * bits_to_decimal(epsilon_rate)


def filter_entries(
    diagnostic_report: DiagnosticReport,
    *,
    criterion: FilterCriterion,
    bit_idx_to_consider: int = 0,
    idxs_to_consider: Optional[List[int]] = None
) -> str:
    """..."""

    if idxs_to_consider is None:
        idxs_to_consider = list(range(len(diagnostic_report)))

    if len(idxs_to_consider) == 1:
        return "".join(diagnostic_report[idxs_to_consider[0]])

    lines_to_consider = [diagnostic_report[idx] for idx in idxs_to_consider]
    bit_counter = Counter(line[bit_idx_to_consider] for line in lines_to_consider)

    [
        (most_common_bit, most_common_freq),
        (least_common_bit, least_common_freq),
    ] = bit_counter.most_common()
    if most_common_freq > least_common_freq:
        if criterion == FilterCriterion.MOST_COMMON:
            bit_to_keep = most_common_bit
        else:
            bit_to_keep = least_common_bit
    else:
        if criterion == FilterCriterion.MOST_COMMON:
            bit_to_keep = "1"
        else:
            bit_to_keep = "0"

    return filter_entries(
        diagnostic_report,
        criterion=criterion,
        bit_idx_to_consider=bit_idx_to_consider + 1,
        idxs_to_consider=[
            idx
            for idx in idxs_to_consider
            if diagnostic_report[idx][bit_idx_to_consider] == bit_to_keep
        ],
    )


def compute_life_support_rating(diagnostic_report: DiagnosticReport) -> int:
    """..."""

    oxygen_rating = filter_entries(
        diagnostic_report, criterion=FilterCriterion.MOST_COMMON
    )
    co2_scrubber_rating = filter_entries(
        diagnostic_report, criterion=FilterCriterion.LEAST_COMMON
    )

    return bits_to_decimal(oxygen_rating) * bits_to_decimal(co2_scrubber_rating)


def part1(input: str) -> int:
    """..."""

    diagnostic_report = parse_diagnostic_report(input)
    return compute_power_consumption(diagnostic_report)


def part2(input: str) -> int:
    """..."""

    diagnostic_report = parse_diagnostic_report(input)
    return compute_life_support_rating(diagnostic_report)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
