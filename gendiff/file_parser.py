import json
import os
import pathlib

import yaml

from gendiff.config import cfg


def get_data(file_path: pathlib.Path) -> dict:
    """Make dict from json or yaml.

    Parameters:
        file_path: path to file

    Returns:
        data from file in dict
    """
    file_extension = get_extension(file_path).lower()
    with open(file_path, 'r') as file_data:
        if file_extension in cfg['file_formats']['json']:
            data = json.load(file_data)
        elif file_extension in cfg['file_formats']['yaml']:
            data = yaml.load(file_data, Loader=yaml.FullLoader)
        else:
            raise ValueError(
                cfg['message']['extension_not_suitable'].format(
                    path=file_path
                )
            )
    return data


def get_extension(file_path: pathlib.Path) -> str:
    """Parse file extention from file path.

    Parameters:
        file_path: path to file

    Returns:
        file extention
    """
    _, file_extension = os.path.splitext(file_path)
    return file_extension
