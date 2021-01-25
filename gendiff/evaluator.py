"""Differences evaluator."""
from gendiff import file_parser
from gendiff.formaters import get_output_string
from typing import Any

STYLISH_FORMAT = 'stylish'
PLAIN_FORMAT = 'plain'
JSON_FORMAT = 'json'

STATUS_ADDED = 'added'
STATUS_REMOVED = 'removed'
STATUS_UPDATED = 'updated'
STATUS_NO_CHANGE = 'no change'
STATUS_NODE = 'node'

STATUS_INDEFINED = 'indefined'

ROOT_KEY = 'root'


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

    diff_data = get_diff(first_file_data, second_file_data)

    diff = get_output_string(diff_data, output_format)

    return diff


def get_diff(
    start_data: dict,
    end_data: dict,
    node_key: str = ROOT_KEY
) -> dict:
    """Generate differences data.

    Parameters:
        start_data: formated dict with data
        end_data: formated dict with data

    Returns:
        formated data with key "diff": add/remove/no_change

    """
    all_keys = start_data.keys() | end_data.keys()
    values = []

    for key in all_keys:
        start_value_exist = key in start_data
        end_value_exist = key in end_data

        if start_value_exist:
            start_value = start_data[key]
        if end_value_exist:
            end_value = end_data[key]

        if start_value_exist and not end_value_exist:
            values.append(get_leaf(
                key, start_value, STATUS_REMOVED
            ))
        elif not start_value_exist and end_value_exist:
            values.append(get_leaf(
                key, end_value, STATUS_ADDED
            ))
        elif start_value_exist and end_value_exist:

            if isinstance(start_value, dict) and isinstance(end_value, dict):
                values.append(
                    get_diff(start_value, end_value, node_key=key)
                )
            elif start_value == end_value:
                values.append(
                    get_leaf(key, start_value, STATUS_NO_CHANGE)
                )
            elif start_value != end_value:
                values.append(
                    get_leaf(
                        key, (start_value, end_value), STATUS_UPDATED
                    )
                )

    diff = {
        'key': node_key,
        'values': values,
        'diff': STATUS_NODE
    }
    return diff


def get_leaf(key: Any, values: Any, diff_status: str) -> dict:
    """Create a new formatted leaf.
    If status is upadted can get two value old and new in tuple.
    """
    if diff_status == STATUS_UPDATED:
        old_values, new_values = values
        leaf = {
            'key': key,
            'old_values': old_values,
            'new_values': new_values,
            'diff': diff_status
        }
    else:
        leaf = {'key': key, 'values': values, 'diff': diff_status}
    return leaf
