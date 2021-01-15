"""Differences evaluator."""
from differences_evaluator import file_parser


def print_diff(
    first_file_path: str,
    second_file_path: str,
    format_output_file: str = None
):
    print(stylish(generate_diff(first_file_path, second_file_path)))


def generate_diff(
    first_file_path: str,
    second_file_path: str
) -> dict:
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json
    """
    first_file_data = file_parser.get_repr(
        file_parser.get_data(first_file_path)
    )
    second_file_data = file_parser.get_repr(
        file_parser.get_data(second_file_path)
    )
    if not first_file_data or not second_file_data:
        return

    diff = get_diff(first_file_data, second_file_data)

    return diff


def get_diff():
    pass


def stylish(diff_data: dict) -> str:
    """Format diff data dict.
     - deleted key: value
     + added key: value
       unchanged key: value

    Parameters:
        diff_data: differences data representation

    Returns:
        formated string
    """
    pass
