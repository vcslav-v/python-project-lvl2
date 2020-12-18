import json
import os

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
