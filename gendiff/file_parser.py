import json
import pathlib

import yaml


def get_data(file_path: pathlib.Path) -> dict:
    """Make dict from json or yaml.

    Parameters:
        file_path: path to file

    Returns:
        data from file in dict
    """
    file_extension = file_path.suffix.lower()
    with open(file_path, 'r') as file_data:
        if file_extension == '.json':
            data = json.load(file_data)
        elif file_extension in ('.yaml', '.yml'):
            data = yaml.load(file_data, Loader=yaml.FullLoader)
        else:
            raise ValueError(
                'File "{path}" is not json or yaml file'.format(path=file_path)
            )
    return data
