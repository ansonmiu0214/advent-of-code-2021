from dataclasses import dataclass, field
import functools
import sys
from typing import Callable, Dict, List, NamedTuple, Protocol, Tuple

from python.util import run_solution


class PacketHeader(NamedTuple):
    version: int
    type_id: int


class Packet(Protocol):
    def version_sum(self) -> int:
        """..."""

    def evaluate(self) -> int:
        """..."""


@dataclass
class LiteralPacket(Packet):
    header: PacketHeader
    value: int

    def version_sum(self) -> int:
        return self.header.version

    def evaluate(self) -> int:
        return self.value


def product(values: List[int]) -> int:
    return functools.reduce(lambda acc, curr: acc * curr, values, 1)


def _binary_operator(values: List[int], *, operator: Callable[[int, int], int]) -> int:
    assert len(values) == 2, f"Expected length ({len(values)}) to be 2"

    first, second = values
    return operator(first, second)


greater_than = functools.partial(
    _binary_operator, operator=lambda first, second: first > second
)

less_than = functools.partial(
    _binary_operator, operator=lambda first, second: first < second
)

equals = functools.partial(
    _binary_operator, operator=lambda first, second: first == second
)


@dataclass
class OperatorPacket(Packet):
    header: PacketHeader
    subpackets: List[Packet]
    operator: Callable[[List[int]], int] = field(init=False)

    def __post_init__(self) -> None:
        """..."""

        operator_packet_strategies: Dict[int, Callable[[List[int]], int]] = {
            0: sum,
            1: product,
            2: min,
            3: max,
            5: greater_than,
            6: less_than,
            7: equals,
        }

        self.operator = operator_packet_strategies[self.header.type_id]

    def version_sum(self) -> int:
        return self.header.version + sum(
            packet.version_sum() for packet in self.subpackets
        )

    def evaluate(self) -> int:
        subpacket_values = [subpacket.evaluate() for subpacket in self.subpackets]
        return self.operator(subpacket_values)


def binary_to_decimal(bits: str) -> int:
    """..."""

    return int(bits, base=2)


def hex_to_binary(hex: str) -> str:
    """..."""

    binary_for_hex = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }

    bits = []
    for digit in hex:
        bits.append(binary_for_hex[digit])

    return "".join(bits)


def _parse_literal_packet(
    bits: str, *, header: PacketHeader, start_index: int
) -> Tuple[LiteralPacket, int]:
    """..."""

    LAST_GROUP_MARKER = "0"
    end_index = start_index

    marker = None
    value_bits = []
    while marker != LAST_GROUP_MARKER:
        marker = bits[end_index]

        end_index += 1
        value_bits.append(bits[end_index : end_index + 4])
        end_index += 4

    packet = LiteralPacket(header=header, value=binary_to_decimal("".join(value_bits)))

    return packet, end_index


def _parse_operator_packet(
    bits: str, *, header: PacketHeader, start_index: int
) -> Tuple[OperatorPacket, int]:
    """..."""

    subpackets = []
    end_index = start_index

    subpacket_indicator = bits[end_index]
    end_index += 1

    if subpacket_indicator == "0":
        subpacket_indicator_size = 15
        total_size_of_subpackets = binary_to_decimal(
            bits[end_index : end_index + subpacket_indicator_size]
        )
        end_index += subpacket_indicator_size

        subpackets_size = 0
        while subpackets_size < total_size_of_subpackets:
            subpacket_start = end_index
            subpacket, end_index = _parse_packet(bits, start_index=subpacket_start)
            subpackets_size += end_index - subpacket_start
            subpackets.append(subpacket)

    else:
        subpacket_indicator_size = 11
        number_of_subpackets = binary_to_decimal(
            bits[end_index : end_index + subpacket_indicator_size]
        )
        end_index += subpacket_indicator_size

        for _ in range(number_of_subpackets):
            subpacket_start = end_index
            subpacket, end_index = _parse_packet(bits, start_index=subpacket_start)
            subpackets.append(subpacket)

    packet = OperatorPacket(header=header, subpackets=subpackets)
    return packet, end_index


def _parse_packet(bits: str, *, start_index: int = 0) -> Tuple[Packet, int]:
    """..."""

    end_index = start_index
    version = binary_to_decimal(bits[end_index : end_index + 3])
    end_index += 3

    type_id = binary_to_decimal(bits[end_index : end_index + 3])
    end_index += 3

    header = PacketHeader(
        version=version,
        type_id=type_id,
    )

    packet_parser = (
        _parse_literal_packet if header.type_id == 4 else _parse_operator_packet
    )
    return packet_parser(bits, header=header, start_index=end_index)


def parse_packet(input: str) -> Packet:
    """..."""

    bits = hex_to_binary(input)
    packet, _ = _parse_packet(bits)

    return packet


def part1(input: str) -> int:
    """..."""

    packet = parse_packet(input)
    return packet.version_sum()


def part2(input: str) -> int:
    """..."""

    packet = parse_packet(input)
    return packet.evaluate()


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
