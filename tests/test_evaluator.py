"""Tests for differences_evaluator"""
import json
import os

import pytest
import yaml
from differences_evaluator import evaluator

from tests.fixtures.jsons import (fake_json, flat_first_json, flat_second_json,
                                  wrong_json)
from tests.fixtures.yamls import (fake_yaml, flat_first_yaml, flat_second_yaml,
                                  wrong_yaml)

with open(
    os.path.join('tests', 'fixtures', 'evaluator_content.json'), 'r'
) as test_content_file:
    test_content = json.load(test_content_file)


def test_get_diff_string():
    result = evaluator.get_diff_string(
        *test_content['test_get_diff_string']['args']
    )
    expect = set(test_content['test_get_diff_string']['expect'])
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    assert result[0] == '{'
    assert result[-1] == '}'
    result = set(result[1:-1])
    assert result == expect


def test_get_diff_string_empty_dicts():
    result = evaluator.get_diff_string(
        *test_content['test_get_diff_string_empty_dicts']['args']
    )
    assert result == test_content['test_get_diff_string_empty_dicts']['expect']


def test_get_diff_string_wrong_attr():
    with pytest.raises(AttributeError):
        evaluator.get_diff_string(
            *test_content['test_get_diff_string_wrong_attr']['args']
        )


def test_generate_diff_json(flat_first_json, flat_second_json):
    expect = set(test_content['test_generate_diff_json']['expect'])
    result = evaluator.generate_diff(flat_first_json, flat_second_json)
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    assert result[0] == '{'
    assert result[-1] == '}'
    result = set(result[1:-1])
    assert result == expect


def test_generate_diff_yaml(flat_first_yaml, flat_second_yaml):
    expect = set(test_content['test_generate_diff_yaml']['expect'])
    result = evaluator.generate_diff(flat_first_yaml, flat_second_yaml)
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    assert result[0] == '{'
    assert result[-1] == '}'
    result = set(result[1:-1])
    assert result == expect


def test_generate_diff_wrong_yaml(flat_first_yaml, wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        evaluator.generate_diff(flat_first_yaml, wrong_yaml)


def test_generate_diff_not_exist_file(flat_first_json, fake_json):
    with pytest.raises(FileNotFoundError):
        evaluator.generate_diff(flat_first_json, fake_json)
