"""Differences evaluator."""
import json
import os
import yaml


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
):
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json
    """
    first_data = get_data(first_file_path)
    second_data = get_data(second_file_path)
    if not first_data or not second_data:
        return

    result = '{\n' + get_diff(first_data, second_data) + '}'

    return result


def get_data(file_path: str) -> dict:
    """Make dict from json or yaml.

    Parameters:
        file_path: path to file

    Returns:
        data from file in dict
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.json':
        with open(file_path, 'r') as json_file:
            file_data = json.load(json_file)
    elif file_extension == '.yaml' or file_extension == '.yml':
        with open(file_path, 'r') as yaml_file:
            file_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    else:
        file_data = None
    return file_data


def get_diff(first_data: dict, second_data: dict) -> str:
    """Generation of the difference in format.
     - deleted key: value
     + added key: value
       unchanged key: value

    Parameters:
        first_data: data dict
        second_data: data dict

    Returns:
        formated string
    """
    result = ''
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
    return result
