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


def test_stylish():
    result = evaluator.stylish(
        *test_content['test_stylish']['args']
    )
    expect = set(test_content['test_stylish']['expect'])
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    assert result[0] == '{'
    assert result[-1] == '}'
    result = set(result[1:-1])
    assert result == expect


def test_stylish_empty_diff():
    result = evaluator.stylish(
        *test_content['test_stylish_empty_diff']['args']
    )
    assert result == test_content['test_stylish_empty_diff']['expect']


def test_stylish_wrong_attr():
    with pytest.raises(AttributeError):
        evaluator.stylish(
            *test_content['test_stylish_wrong_attr']['args']
        )


def test_get_diff():
    result = evaluator.get_diff(
        *test_content['test_get_diff']['args']
    )
    assert result == test_content['test_get_diff']['expect']


def test_get_diff_wrong_args():
    pass


def test_get_diff_wrong_format_args():
    pass


def test_get_diff_empty():
    result = evaluator.get_diff(
        *test_content['test_get_diff_empty']['args']
    )
    assert result == test_content['test_get_diff_empty']['expect']


def test_generate_diff_flat_json(flat_first_json, flat_second_json):
    result = evaluator.generate_diff(flat_first_json, flat_second_json)
    assert result == test_content['test_generate_diff_flat_json']['expect']


def test_generate_diff_flat_yaml(flat_first_yaml, flat_second_yaml):
    result = evaluator.generate_diff(flat_first_yaml, flat_second_yaml)
    assert result == test_content['test_generate_diff_flat_yaml']['expect']


def test_generate_diff_tree_json(tree_first_json, tree_second_json):
    result = evaluator.generate_diff(tree_first_json, tree_second_json)
    assert result == test_content['test_generate_diff_tree_json']['expect']


def test_generate_diff_tree_yaml(tree_first_yaml, tree_second_yaml):
    result = evaluator.generate_diff(tree_first_yaml, tree_second_yaml)
    assert result == test_content['test_generate_diff_tree_yaml']['expect']


def test_generate_diff_wrong_yaml(flat_first_yaml, wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        evaluator.generate_diff(flat_first_yaml, wrong_yaml)


def test_generate_diff_not_exist_file(flat_first_json, fake_json):
    with pytest.raises(FileNotFoundError):
        evaluator.generate_diff(flat_first_json, fake_json)
