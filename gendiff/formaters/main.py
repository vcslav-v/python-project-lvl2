"""Formaters."""
from gendiff.formaters.stylish import stylish
from gendiff.formaters.plain import plain
from gendiff.formaters.json_formater import json_formater

STYLISH_FORMAT = 'stylish'
PLAIN_FORMAT = 'plain'
JSON_FORMAT = 'json'

FORMAT_NOT_SUITABLE = 'The format "{format}" is not supported'


def get_output_string(diff_data: dict, output_format: str) -> str:

    if output_format == STYLISH_FORMAT:
        diff = stylish(diff_data)
    elif output_format == PLAIN_FORMAT:
        diff = plain(diff_data)
    elif output_format == JSON_FORMAT:
        diff = json_formater(diff_data)
    else:
        raise ValueError(
            FORMAT_NOT_SUITABLE.format(
                format=output_format
            )
        )

    return diff
