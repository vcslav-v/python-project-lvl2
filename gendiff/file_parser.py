"""Parser json/yaml file data."""
import json
import os

import yaml

JSON = ('.json')
YAML = ('.yaml', '.yml')
EXTENSION_NOT_SUITABLE = 'File "{path}" is not json or yaml file'


def get_data(file_path: str) -> dict:
    """Make dict from json or yaml.

    Parameters:
        file_path: path to file

    Returns:
        data from file in dict
    """
    file_extension = get_extension(file_path).lower()
    with open(file_path, 'r') as file_data:
        if file_extension in JSON:
            data = json.load(file_data)
        elif file_extension in YAML:
            data = yaml.load(file_data, Loader=yaml.FullLoader)
        else:
            raise ValueError(
                EXTENSION_NOT_SUITABLE.format(
                    path=file_path
                )
            )
    return data


def get_extension(file_path: str) -> str:
    """Parse file extention from file path.

    Parameters:
        file_path: path to file

    Returns:
        file extention
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension
