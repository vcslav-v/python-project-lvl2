#!/usr/bin/env python3
"""Generator differences run script."""

import argparse
from typing import Tuple

from gendiff import evaluator
from gendiff.formaters import JSON_FORMAT, PLAIN_FORMAT, STYLISH_FORMAT

DESCRIPTION = 'Generate diff'
HELP_STRING = 'set format of output'


def main():
    first_file, second_file, output_format = get_arguments()
    try:
        print(evaluator.generate_diff(
            first_file, second_file, output_format)
        )
    except Exception as e:
        print(e)


def get_arguments() -> Tuple[str, str, str]:
    """Take the command-line arguments.
    first_file, second_file, output_format

    Returns:
        (first_file, second_file, output_format)
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument(
        '-f', '--format',
        help=HELP_STRING,
        type=str,
        default=STYLISH_FORMAT,
        choices=[
            STYLISH_FORMAT,
            PLAIN_FORMAT,
            JSON_FORMAT
        ]
    )
    args = parser.parse_args()
    return (str(args.first_file), str(args.second_file), str(args.format))


if __name__ == "__main__":
    main()
