#!/usr/bin/env python3
"""Generator differences run script."""

import argparse
import pathlib
from gendiff import evaluator


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument('first_file', type=pathlib.Path)
    parser.add_argument('second_file', type=pathlib.Path)
    parser.add_argument(
        '-f', '--format',
        help='set format of output',
        type=str,
        default='stylish',
        choices=['stylish', 'plain', 'json']
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
