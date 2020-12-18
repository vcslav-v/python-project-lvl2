"""Tests for differences_evaluator"""
import json
import os

import pytest
import yaml
from differences_evaluator import evaluator

from tests.fixtures.jsons import fake_json, first_json, second_json, wrong_json
from tests.fixtures.yamls import fake_yaml, first_yaml, second_yaml, wrong_yaml

with open(
    os.path.join('tests', 'fixtures', 'expect.json'), 'r'
) as expects:
    expects = json.load(expects)


def test_get_diff_string():
    result = evaluator.get_diff_string(
        {
            'host': 'hexlet.io',
            'timeout': 50,
            'proxy': '123.234.53.22',
            'follow': False
        },
        {
            'timeout': 20,
            'verbose': True,
            'host': 'hexlet.io'
        }
    )
    expect = set(expects['test_values_generate_diff'])
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    assert result[0] == '{'
    assert result[-1] == '}'
    result = set(result[1:-1])
    assert result == expect


def test_get_diff_string_empty_dicts():
    result = evaluator.get_diff_string({}, {})
    assert result == '{\n}'


def test_get_diff_string_wrong_attr():
    with pytest.raises(AttributeError):
        evaluator.get_diff_string(0, [0])


def test_generate_diff_json(first_json, second_json):
    expect = set(expects['test_values_generate_diff'])
    result = evaluator.generate_diff(first_json, second_json)
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    assert result[0] == '{'
    assert result[-1] == '}'
    result = set(result[1:-1])
    assert result == expect


def test_generate_diff_yaml(first_yaml, second_yaml):
    expect = set(expects['test_values_generate_diff'])
    result = evaluator.generate_diff(first_yaml, second_yaml)
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    assert result[0] == '{'
    assert result[-1] == '}'
    result = set(result[1:-1])
    assert result == expect


def test_generate_diff_wrong_yaml(first_yaml, wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        evaluator.generate_diff(first_yaml, wrong_yaml)


def test_generate_diff_not_exist_file(first_json, fake_json):
    with pytest.raises(FileNotFoundError):
        evaluator.generate_diff(first_json, fake_json)
