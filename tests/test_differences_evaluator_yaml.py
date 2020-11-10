"""Tests for differences_evaluator"""
import json
import yaml
import os

import pytest

from differences_evaluator import evaluator

from tests.fixtures.yamls import first_yaml, second_yaml, wrong_yaml, fake_yaml


def test_format_generate_diff(first_yaml, second_yaml):
    result = evaluator.generate_diff(first_yaml, second_yaml)
    assert (result[0], result[-1]) == ('{', '}')


def test_values_generate_diff(first_yaml, second_yaml):
    with open(
        os.path.join('tests', 'fixtures', 'expect.json'), 'r'
    ) as expects:
        expects_json = json.load(expects)
    expect = set(expects_json['test_values_generate_diff'])
    result = evaluator.generate_diff(first_yaml, second_yaml)
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    result = set(result[1:-1])
    assert result == expect


def test_wrong_yaml_exceptions_generate_diff(first_yaml, wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        evaluator.generate_diff(first_yaml, wrong_yaml)


def test_not_exist_exceptions_yaml_generate_diff(first_yaml, fake_yaml):
    with pytest.raises(FileNotFoundError):
        evaluator.generate_diff(first_yaml, fake_yaml)
