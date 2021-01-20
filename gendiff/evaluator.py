"""Differences evaluator."""
from gendiff import file_parser, formaters
import pathlib


def generate_diff(
    first_file_path: pathlib.Path,
    second_file_path: pathlib.Path,
    format_output_file: str = 'stylish'
) -> str:
    """Generate diffirences of two files.

    Parameters:
        first_file_path: path to first target file
        second_file_path: path to second target file
        format_file: format needed plain or json
    """
    first_file_data = file_parser.get_data(first_file_path)
    second_file_data = file_parser.get_data(second_file_path)
    diff = get_diff(first_file_data, second_file_data)
    if format_output_file == 'stylish':
        return(formaters.stylish(diff))
    elif format_output_file == 'plain':
        return formaters.plain(diff)
    elif format_output_file == 'json':
        return formaters.json_diff_formater(diff)


def sort_diff(diff):
    diff['value'] = sorted(diff['value'], key=lambda value: value['key'])

    for i in range(len(diff['value']) - 1):
        if diff['value'][i]['key'] == diff['value'][i + 1]['key']:
            if diff['value'][i]['diff'] == 'added':
                diff['value'][i], diff['value'][i + 1] = (
                    diff['value'][i + 1], diff['value'][i]
                )
    return diff


def get_leaf(key, value, diff_status):
    return {'key': key, 'value': value, 'type': 'leaf', 'diff': diff_status}


def get_diff(
    start_data: dict = None,
    end_data: dict = None,
    node_key: str = 'root'
) -> dict:
    """Generate differences data.

    Parameters:
        start_data: formated dict with data
        end_data: formated dict with data

    Returns:
        formated data with key "diff": add/remove/no change

    """
    diff_status = {
        'added': 'added',
        'removed': 'removed',
        'no change': 'no change',
    }
    diff = {
        'key': node_key,
        'value': [],
        'type': 'node',
        'diff': diff_status['no change']
    }
    all_keys = set(start_data.keys()).union(set(end_data.keys()))
    for key in all_keys:

        try:
            start_value = start_data[key]
        except KeyError:
            #  the key with the node was added
            end_value = end_data[key]
            diff['value'].append(get_leaf(
                key, end_value, diff_status['added']
            )
            )
            continue

        try:
            end_value = end_data[key]
        except KeyError:
            #  the key with the node was removed
            diff['value'].append(get_leaf(
                key, start_value, diff_status['removed']
            )
            )
            continue

        if type(start_value) is dict and type(end_value) is dict:
            #  there are children in both nodes
            diff['value'].append(
                get_diff(start_value, end_value, node_key=key)
            )
            continue

        if start_value == end_value:
            diff['value'].append(
                get_leaf(key, start_value, diff_status['no change'])
            )
        elif start_value != end_value:
            diff['value'].append(
                get_leaf(key, start_value, diff_status['removed'])
            )
            diff['value'].append(
                get_leaf(key, end_value, diff_status['added'])
            )

    diff = sort_diff(diff)
    return diff
