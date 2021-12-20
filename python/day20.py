import sys
from typing import Generator, List, Tuple

from python.util import run_solution


Algorithm = List[int]
Image = List[List[int]]

LIGHT_PIXEL = "#"


def pixel_to_binary(pixel: str) -> int:
    """..."""

    return int(pixel == LIGHT_PIXEL)


def parse_algorithm(input: str) -> Algorithm:
    """..."""

    return list(map(pixel_to_binary, input))


def parse_image(input: str) -> Image:
    """..."""

    return [list(map(pixel_to_binary, line)) for line in input.splitlines()]


def parse_input(input: str) -> Tuple[Algorithm, Image]:
    """..."""

    algorithm_input, image_input = input.split("\n\n")

    algorithm = parse_algorithm(algorithm_input)
    image = parse_image(image_input)

    return algorithm, image


def dimensions(image: Image) -> Tuple[int, int]:
    """..."""

    num_rows = len(image)
    num_cols = len(image[0])

    return num_rows, num_cols


def pixel_window(
    row: int, col: int, *, length: int
) -> Generator[Tuple[int, int], None, None]:
    """..."""

    assert length % 2 == 1, f"Expected length ({length}) to be odd"

    delta_from_center = length // 2

    for row_delta in range(-delta_from_center, delta_from_center + 1):
        for col_delta in range(-delta_from_center, delta_from_center + 1):
            yield (row + row_delta, col + col_delta)


def get_pixel(image: Image, *, row: int, col: int, background_color: int) -> int:
    """..."""

    num_rows, num_cols = dimensions(image)
    if 0 <= row < num_rows and 0 <= col < num_cols:
        return image[row][col]

    return background_color


def compute_new_background_color(
    background_color: int, *, algorithm: Algorithm, window_length: int
) -> int:
    """..."""

    index = int(str(background_color) * window_length, 2)
    return algorithm[index]


def apply_algorithm(
    image: Image, *, algorithm: Algorithm, background_color: int, window_length: int
) -> Tuple[Image, int]:
    """..."""

    assert window_length % 2, f"Expected window_length ({window_length}) to be odd"

    padding = window_length // 2

    num_rows, num_cols = dimensions(image)
    new_image = [
        [None for _ in range(num_cols + 2 * padding)]
        for _ in range(num_rows + 2 * padding)
    ]

    for row in range(-padding, num_rows + padding):
        for col in range(-padding, num_cols + padding):
            window = pixel_window(row, col, length=window_length)

            enhanced_bits = [
                get_pixel(image, row=x, col=y, background_color=background_color)
                for x, y in window
            ]
            index = int("".join(map(str, enhanced_bits)), 2)

            new_image[row + padding][col + padding] = algorithm[index]

    new_background_color = compute_new_background_color(
        background_color, algorithm=algorithm, window_length=window_length
    )

    return new_image, new_background_color


def count_lit_pixels(image: Image) -> int:
    """..."""

    num_rows, num_cols = dimensions(image)

    return sum(image[row][col] for row in range(num_rows) for col in range(num_cols))


def print_image(image: Image) -> None:
    """..."""

    for row in image:
        for col in row:
            print("#" if col else ".", end="")
        print()


def apply_algorithm_n_times(
    image: Image,
    *,
    algorithm: Algorithm,
    window_length: int,
    iterations: int,
) -> Image:
    """..."""

    background_color = 0

    for _ in range(iterations):
        image, background_color = apply_algorithm(
            image,
            algorithm=algorithm,
            background_color=background_color,
            window_length=window_length,
        )

    return image


def part1(input: str) -> int:
    """..."""

    algorithm, image = parse_input(input)

    output_image = apply_algorithm_n_times(
        image, algorithm=algorithm, window_length=3, iterations=2
    )

    return count_lit_pixels(output_image)


def part2(input: str) -> int:
    """..."""

    algorithm, image = parse_input(input)

    output_image = apply_algorithm_n_times(
        image, algorithm=algorithm, window_length=3, iterations=50
    )

    return count_lit_pixels(output_image)


if __name__ == "__main__":
    sys.exit(run_solution(part1=part1, part2=part2))
