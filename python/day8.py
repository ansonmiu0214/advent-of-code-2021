import sys
from typing import Dict, List, NamedTuple, Set

from python.util import run_solution


# Reference
# ---------
# Each digit of a seven-segment display is rendered by turning on or off any of
# seven segments named a through g:
# ..
#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
# ..


Segment = str


class Display(NamedTuple):
    digit_segments: List[Segment]
    output_values: List[Segment]


def parse_segments(line: str) -> List[Segment]:
    """..."""

    return list(filter(None, line.split(" ")))


def parse_display(line: str) -> Display:
    """..."""

    digit_segments_input, output_values_input = line.split("|")
    return Display(
        digit_segments=parse_segments(digit_segments_input),
        output_values=parse_segments(output_values_input),
    )


def normalise_segment(segment: str) -> str:
    """..."""

    return "".join(sorted(segment))


def segments_with_unique_digit_count(
    segments: List[Segment], *, count: int
) -> List[Segment]:
    """..."""

    return [segment for segment in segments if len(segment) == count]


def decode_display(display: Display) -> int:
    """..."""

    digit_segments, output_values = display

    encoding_base_to_display: Dict[str, str] = {}
    segment_chars_to_number: Dict[str, int] = {}

    # Start with decoding {1,4,7,8} since they use an unique number of digits.

    [one_segment] = segments_with_unique_digit_count(digit_segments, count=2)
    segment_chars_to_number[normalise_segment(one_segment)] = 1

    [seven_segment] = segments_with_unique_digit_count(digit_segments, count=3)
    segment_chars_to_number[normalise_segment(seven_segment)] = 7

    encoding_base_to_display["a"] = next(iter(set(seven_segment) - set(one_segment)))

    [four_segment] = segments_with_unique_digit_count(digit_segments, count=4)
    segment_chars_to_number[normalise_segment(four_segment)] = 4

    [eight_segment] = segments_with_unique_digit_count(digit_segments, count=7)
    segment_chars_to_number[normalise_segment(eight_segment)] = 8

    # Decode {0,6,9}, which all use 6 unique digits.

    b_d = set(four_segment) - set(seven_segment)
    c_f = set(one_segment)

    zero_six_nine = segments_with_unique_digit_count(digit_segments, count=6)
    b_d_c_f_a = b_d | c_f | {encoding_base_to_display["a"]}

    [nine_segment] = [
        segment for segment in zero_six_nine if b_d_c_f_a.issubset(set(segment))
    ]
    segment_chars_to_number[normalise_segment(nine_segment)] = 9

    encoding_base_to_display["g"] = next(iter(set(nine_segment) - b_d_c_f_a))

    [six_segment] = [
        segment
        for segment in zero_six_nine
        if segment != nine_segment and b_d.issubset(set(segment))
    ]
    segment_chars_to_number[normalise_segment(six_segment)] = 6

    zero_segment = next(iter(set(zero_six_nine) - {six_segment, nine_segment}))
    segment_chars_to_number[normalise_segment(zero_segment)] = 0

    # Decode {2,3,5}, which all use 5 unique digits.

    two_three_five = segments_with_unique_digit_count(digit_segments, count=5)

    [three_segment] = [segment for segment in two_three_five if c_f.issubset(segment)]
    segment_chars_to_number[normalise_segment(three_segment)] = 3

    encoding_base_to_display["b"] = next(iter(set(nine_segment) - set(three_segment)))

    [five_segment] = [
        segment
        for segment in two_three_five
        if encoding_base_to_display["b"] in segment
    ]
    segment_chars_to_number[normalise_segment(five_segment)] = 5

    two_segment = next(iter(set(two_three_five) - {five_segment, three_segment}))
    segment_chars_to_number[normalise_segment(two_segment)] = 2

    # Decode the digits using the 'segment_chars_to_number' lookup table.

    decoded_digits = [
        segment_chars_to_number[normalise_segment(digit)] for digit in output_values
    ]

    return int("".join(map(str, decoded_digits)))


def count_digits_in_display(display: Display, *, digits: Set[int]) -> int:
    """..."""

    output_value = decode_display(display)
    return sum(str(output_value).count(str(digit)) for digit in digits)


def part1(input: str) -> int:
    """..."""

    displays = list(map(parse_display, input.splitlines()))
    return sum(
        count_digits_in_display(display, digits={1, 4, 7, 8}) for display in displays
    )


def part2(input: str) -> int:
    """..."""

    displays = list(map(parse_display, input.splitlines()))
    return sum(map(decode_display, displays))


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
