"""Tests for differences_evaluator"""
import json
import os

import pytest

from differences_evaluator import evaluator

from tests.fixtures.jsons import first_json, second_json, wrong_json, fake_json


def test_format_generate_diff(first_json, second_json):
    result = evaluator.generate_diff(first_json, second_json)
    assert (result[0], result[-1]) == ('{', '}')


def test_values_generate_diff(first_json, second_json):
    with open(
        os.path.join('tests', 'fixtures', 'expect.json'), 'r'
    ) as expects:
        expects_json = json.load(expects)
    expect = set(expects_json['test_values_generate_diff'])
    result = evaluator.generate_diff(first_json, second_json)
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    result = set(result[1:-1])
    assert result == expect


def test_wrong_json_exceptions_json_generate_diff(first_json, wrong_json):
    with pytest.raises(json.JSONDecodeError):
        evaluator.generate_diff(first_json, wrong_json)


def test_not_exist_exceptions_json_generate_diff(first_json, fake_json):
    with pytest.raises(FileNotFoundError):
        evaluator.generate_diff(first_json, fake_json)
