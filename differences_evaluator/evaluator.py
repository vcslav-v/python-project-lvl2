"""Differences evaluator."""
from differences_evaluator import file_parser, formaters
import pathlib


def generate_diff(
    first_file_path: pathlib.Path,
    second_file_path: pathlib.Path,
    format_output_file: str
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


def get_diff_force(data: dict, node: str, diff_status: str):
    result = {
        'node': node, 'leafs': [], 'children': [], 'diff': diff_status
        }
    for key, value in data.items():
        if type(value) is dict:
            result['children'].append(get_diff_force(
                data=value,
                node=key,
                diff_status=diff_status
                )
            )
        else:
            result['leafs'].append(
                {'key': key, 'value': value, 'diff': diff_status}
                )
    return result


def get_leaf(key, value, diff_status):
    return {'key': key, 'value': value, 'diff': diff_status}


def get_diff(
    start_data: dict = None,
    end_data: dict = None,
    node: str = 'root'
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
        'node': node,
        'leafs': [],
        'children': [],
        'diff': diff_status['no change']
        }
    for key, start_value in start_data.items():
        if type(start_value) is dict:
            try:
                end_value = end_data.pop(key)
            except KeyError:
                #  the key with the node was removed
                diff['children'].append(
                    get_diff_force(
                        start_value, key, diff_status['removed']
                        )
                    )
                continue

            if type(end_value) is dict:
                #  there are children in both nodes
                diff['children'].append(
                    get_diff(start_value, end_value, node=key)
                    )
            else:
                #  the children in start_data have been replaced with the value
                diff['children'].append(
                    get_diff_force(
                        start_value, key, diff_status['removed']
                    )
                )
                diff['leafs'].append(
                    get_leaf(key, end_value, diff_status['added'])
                )
            continue

        try:
            end_value = end_data.pop(key)
        except KeyError:
            #  the key with the value was removed
            diff['leafs'].append(
                get_leaf(key, start_value, diff_status['removed'])
                )
            continue

        if type(end_value) is dict:
            #  the value in start_data have been replaced with the children
            diff['leafs'].append(
                get_leaf(key, start_value, diff_status['removed'])
            )
            diff['children'].append(
                get_diff_force(end_value, key, diff_status['added'])
            )
            continue

        if start_value == end_value:
            diff['leafs'].append(
                get_leaf(key, start_value, diff_status['no change'])
                )
        elif start_value != end_value:
            diff['leafs'].append(
                get_leaf(key, start_value, diff_status['removed'])
                )
            diff['leafs'].append(
                get_leaf(key, end_value, diff_status['added'])
                )

    for key, end_value in end_data.items():
        if type(end_value) is dict:
            diff['children'].append(
                get_diff_force(end_value, key, diff_status['added'])
                )
        else:
            diff['leafs'].append(
                get_leaf(key, end_value, diff_status['added'])
                )

    return diff
