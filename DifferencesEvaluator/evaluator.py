"""Differences evaluator."""
import json

def print_diff(first_file_path: str, second_file_path: str, format_file: str):
    print(generate_diff(first_file_path, second_file_path, format_file))


def generate_diff(first_file_path: str, second_file_path: str, format_file: str):
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json 
    """
    if not format_file:
        format_file = 'json'
    
    if format_file == 'json':
        first_data = json.load(open(first_file_path))
        second_data = json.load(open(second_file_path))
        result = '\n{\n'
    for key, value in first_data.items():
        second_value = second_data.get(key)
        pattern = ' {key}: {value}\n'
        if not second_value:
            result += '  -' + pattern.format(key=key, value=value)
        elif value == second_value:
            result += '   ' + pattern.format(key=key, value=value)
        elif value != second_value:
            result += '  -' + pattern.format(key=key, value=value)
            result += '  +' + pattern.format(key=key, value=second_value)
    result += '}'
    return result