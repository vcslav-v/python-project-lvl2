"""Differences evaluator."""
from differences_evaluator import file_parser


def print_diff(
    first_file_path: str,
    second_file_path: str,
    format_output_file: str = None
):
    print(generate_diff(first_file_path, second_file_path, format_output_file))


def generate_diff(
    first_file_path: str,
    second_file_path: str,
    format_output_file: str = None,
) -> str:
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json
    """
    first_data = file_parser.get_data(first_file_path)
    second_data = file_parser.get_data(second_file_path)
    if not first_data or not second_data:
        return

    result = get_diff_string(first_data, second_data)

    return result


def get_diff_string(first_data: dict, second_data: dict) -> str:
    """Generation of the difference in format.
     - deleted key: value
     + added key: value
       unchanged key: value

    Parameters:
        first_data: first data dict
        second_data: second data dict

    Returns:
        formated string
    """
    result = '{\n'
    set_of_keys = set(first_data.keys()).union(set(second_data.keys()))
    for key in set_of_keys:
        first_value = first_data.get(key)
        second_value = second_data.get(key)
        pattern = ' {key}: {value}\n'
        if not second_value:
            result += '  -' + pattern.format(key=key, value=first_value)
        elif not first_value:
            result += '  +' + pattern.format(key=key, value=second_value)
        elif first_value == second_value:
            result += '   ' + pattern.format(key=key, value=first_value)
        elif first_value != second_value:
            result += '  -' + pattern.format(key=key, value=first_value)
            result += '  +' + pattern.format(key=key, value=second_value)
    result = result + '}'
    return result
