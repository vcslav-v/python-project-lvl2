#!/usr/bin/env python3
"""Generator differences run script."""

import argparse
import pathlib
from gendiff import evaluator
from gendiff.config import cfg


def main():
    parser = argparse.ArgumentParser(description=cfg['message']['description'])
    parser.add_argument('first_file', type=pathlib.Path)
    parser.add_argument('second_file', type=pathlib.Path)
    parser.add_argument(
        '-f', '--format',
        help=cfg['message']['help_string'],
        type=str,
        default=cfg['output_format']['stylish'],
        choices=[
            cfg['output_format']['stylish'],
            cfg['output_format']['plain'],
            cfg['output_format']['json']
        ]
    )
    args = parser.parse_args()

    try:
        print(evaluator.generate_diff(
            args.first_file, args.second_file, args.format)
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
