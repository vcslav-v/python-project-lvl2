"""Formaters."""
from gendiff.formaters import stylish, plain, json_formater

STYLISH_FORMAT = 'stylish'
PLAIN_FORMAT = 'plain'
JSON_FORMAT = 'json'


def get_output_string(diff_data: dict, output_format: str) -> str:

    if output_format == STYLISH_FORMAT:
        diff = stylish(diff_data)
    elif output_format == PLAIN_FORMAT:
        diff = plain(diff_data)
    elif output_format == JSON_FORMAT:
        diff = json_formater(diff_data)

    return diff
