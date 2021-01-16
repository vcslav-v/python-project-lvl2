"""Tests for differences_evaluator"""
import json
import os

import pytest
import yaml
from differences_evaluator import evaluator

from tests.fixtures.jsons import (fake_json, flat_first_json, flat_second_json,
                                  wrong_json,tree_first_json, tree_second_json)
from tests.fixtures.yamls import (fake_yaml, flat_first_yaml, flat_second_yaml,
                                  wrong_yaml, tree_first_yaml,tree_second_yaml)

with open(
    os.path.join('tests', 'fixtures', 'evaluator_content.json'), 'r'
) as test_content_file:
    test_content = json.load(test_content_file)


def compare_node(node, expect):
    for leaf in node['leafs']:
        assert leaf in expect['leafs']
    children_of_node = {}
    children_of_expect = {}
    node['leafs'] = expect['leafs']

    for child in node['children']:
        children_of_node[child['node']] = child
    for child in expect['children']:
        children_of_expect[child['node']] = child

    assert set(children_of_node.keys()) == set(children_of_expect.keys())

    for child_key in children_of_node:
        compare_node(
            children_of_node[child_key], children_of_expect[child_key]
        )
    node['children'] = expect['children']
    assert node == expect


def test_generate_diff_flat_json(flat_first_json, flat_second_json):
    result = evaluator.generate_diff(flat_first_json, flat_second_json)
    for leaf in result['leafs']:
        assert leaf in test_content['test_generate_diff_flat_json']['expect']['leafs']
    result['leafs'] = test_content['test_generate_diff_flat_json']['expect']['leafs']
    assert result == test_content['test_generate_diff_flat_json']['expect']


def test_generate_diff_flat_yaml(flat_first_yaml, flat_second_yaml):
    result = evaluator.generate_diff(flat_first_yaml, flat_second_yaml)
    for leaf in result['leafs']:
        assert leaf in test_content['test_generate_diff_flat_yaml']['expect']['leafs']
    result['leafs'] = test_content['test_generate_diff_flat_yaml']['expect']['leafs']
    assert result == test_content['test_generate_diff_flat_yaml']['expect']


def test_generate_diff_tree_json(tree_first_json, tree_second_json):
    result = evaluator.generate_diff(tree_first_json, tree_second_json)
    compare_node(
        result,
        test_content['test_generate_diff_tree_json']['expect']
    )


def test_generate_diff_tree_yaml(tree_first_yaml, tree_second_yaml):
    result = evaluator.generate_diff(tree_first_yaml, tree_second_yaml)
    compare_node(
        result,
        test_content['test_generate_diff_tree_yaml']['expect']
    )


def test_generate_diff_wrong_yaml(flat_first_yaml, wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        evaluator.generate_diff(flat_first_yaml, wrong_yaml)


def test_generate_diff_not_exist_file(flat_first_json, fake_json):
    with pytest.raises(FileNotFoundError):
        evaluator.generate_diff(flat_first_json, fake_json)


def test_stylish():
    result = evaluator.stylish(
        *test_content['test_stylish']['args']
    )
    expect = set(test_content['test_stylish']['expect'])
    result = result.strip()
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
