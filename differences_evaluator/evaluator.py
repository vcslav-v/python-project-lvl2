"""Differences evaluator."""
import json


def print_diff(
    first_file_path: str,
    second_file_path: str,
    format_file: str = None
):
    print(generate_diff(first_file_path, second_file_path, format_file))


def generate_diff(
    first_file_path: str,
    second_file_path: str,
    format_file: str = None,
):
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json
    """
    #  FIXME
    if not format_file:
        format_file = 'json'
    if format_file == 'json':
        with open(first_file_path, 'r') as json_file:
            first_data = json.load(json_file)
        with open(second_file_path, 'r') as json_file:
            second_data = json.load(json_file)
    else:
        return
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
    result += '}'
    return result
