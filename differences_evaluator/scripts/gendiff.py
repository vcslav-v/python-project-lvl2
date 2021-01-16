#!/usr/bin/env python3
"""Generator differences run script."""

import argparse

from differences_evaluator import evaluator

parser = argparse.ArgumentParser(description='Generate diff')

parser.add_argument('first_file')
parser.add_argument('second_file')

parser.add_argument('-f', '--format', help='set format of output')

args = parser.parse_args()


def main():
    print(evaluator.generate_diff(
        args.first_file, args.second_file, args.format)
    )


if __name__ == "__main__":
    main()
