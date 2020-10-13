#!/usr/bin/env python3
"""Generator differences run script."""

import argparse

from DifferencesEvaluator import evaluator

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')

args = parser.parse_args()


def main():
    evaluator.get_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    main()
