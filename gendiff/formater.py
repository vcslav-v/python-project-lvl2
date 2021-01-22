"""Formaters."""
from gendiff.config import cfg
from gendiff.formaters import stylish, plain, json_formater


def get_output_string(diff_data: dict, output_format: str) -> str:

    if output_format == cfg['output_format']['stylish']:
        diff = stylish(diff_data)
    elif output_format == cfg['output_format']['plain']:
        diff = plain(diff_data)
    elif output_format == cfg['output_format']['json']:
        diff = json_formater(diff_data)

    return diff
