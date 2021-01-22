"""Differences evaluator."""
import pathlib

from gendiff import file_parser, formater
from gendiff.config import cfg


def generate_diff(
    first_file_path: pathlib.Path,
    second_file_path: pathlib.Path,
    output_format: str = cfg['output_format']['stylish']
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

    diff = formater.get_output_string(diff_data, output_format)

    return diff


def sort_diff(value):
    value = sorted(value, key=lambda value: value['key'])
    return value


def get_leaf(key, value, diff_status):
    if diff_status == cfg['diff_status']['updated']:
        old_value, new_value = value
        leaf = {
            'key': key,
            'old_value': old_value,
            'new_value': new_value,
            'diff': diff_status
        }
    else:
        leaf = {'key': key, 'value': value, 'diff': diff_status}
    return leaf


def get_diff(
    start_data: dict,
    end_data: dict,
    node_key: str = cfg['diff_format']['root']
) -> dict:
    """Generate differences data.

    Parameters:
        start_data: formated dict with data
        end_data: formated dict with data

    Returns:
        formated data with key "diff": add/remove/no_change

    """
    diff_status = cfg['diff_status']
    all_keys = start_data.keys() | end_data.keys()
    value = []

    for key in all_keys:
        start_value_exist = False
        end_value_exist = False

        if key in start_data:
            start_value = start_data[key]
            start_value_exist = True
        if key in end_data:
            end_value = end_data[key]
            end_value_exist = True

        if start_value_exist and not end_value_exist:
            #  the key with the node was added
            value.append(get_leaf(
                key, start_value, diff_status['removed']
            ))
        elif end_value_exist and not start_value_exist:
            #  the key with the node was removed
            value.append(get_leaf(
                key, end_value, diff_status['added']
            ))
        elif start_value_exist and end_value_exist:
            if isinstance(start_value, dict) and isinstance(end_value, dict):
                #  there are children in both nodes
                value.append(
                    get_diff(start_value, end_value, node_key=key)
                )
            elif start_value == end_value:
                value.append(
                    get_leaf(key, start_value, diff_status['no_change'])
                )
            elif start_value != end_value:
                value.append(
                    get_leaf(
                        key, (start_value, end_value), diff_status['updated']
                    )
                )

    value = sort_diff(value)
    diff = {
        'key': node_key,
        'value': value,
        'diff': diff_status['node']
    }
    return diff
