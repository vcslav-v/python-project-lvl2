"""Differences evaluator."""
from gendiff import file_parser, diff_builder
from gendiff.formaters import get_output_string, STYLISH_FORMAT


def generate_diff(
    first_file_path: str,
    second_file_path: str,
    output_format: str = STYLISH_FORMAT
) -> str:
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json
    """
    first_file_data = file_parser.get_data(first_file_path)
    second_file_data = file_parser.get_data(second_file_path)

    diff_data = diff_builder.get_diff(first_file_data, second_file_data)

    diff = get_output_string(diff_data, output_format)

    return diff
