import json
import os
from typing import List

import yaml


def get_data(file_path: str) -> dict:
    """Make dict from json or yaml.

    Parameters:
        file_path: path to file

    Returns:
        data from file in dict
    """
    file_extension = get_extension(file_path)
    with open(file_path, 'r') as file_data:
        if file_extension == 'json':
            data = json.load(file_data)
        elif file_extension in ('yaml', 'yml'):
            data = yaml.load(file_data, Loader=yaml.FullLoader)
        else:
            data = None
    return data


def get_extension(file_path: str) -> str:
    """Parse file extention from file path.

    Parameters:
        file_path: path to file

    Returns:
        file extention
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension[1:]


def get_repr(
    data: dict,
    node: str = 'root',
    path: List['str'] = []
) -> dict:
    """Make inner representation tree from data dict.

    Parameters:
        data: data from file
        node: name of node

    Returns:
        representation tree with two type object
        node - {'node': 'node', 'leafs': {}, 'children':[], 'path':()}
        leaf - {'key': 'value'}
    """
    result = {'node': node, 'leafs': {}, 'children': [], 'path': path}

    new_path = path.copy()
    new_path.append(node)

    for key, value in data.items():
        if type(value) is dict:
            result['children'].append(get_repr(value, key, new_path))
        else:
            result['leafs'][key] = value
    return result
