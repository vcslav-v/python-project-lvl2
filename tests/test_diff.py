"""Tests for gendiff"""
import json
import os

from gendiff import evaluator, file_parser

with open(
    os.path.join('tests', 'fixtures', 'evaluator_content.json'), 'r'
) as test_content_file:
    test_content = json.load(test_content_file)


def test_generate_diff_stylish(tree_first_json, tree_second_json):
    result = evaluator.generate_diff(
        tree_first_json, tree_second_json, 'stylish'
    )
    expect = set(test_content['test_generate_diff_stylish']['expect'])
    result = result.split('\n')
    result = set(map(lambda line: line.strip(), result))
    assert result == expect


def test_generate_diff_plain(tree_first_json, tree_second_json):
    result = evaluator.generate_diff(
        tree_first_json, tree_second_json, 'plain'
    )
    expect = set(test_content['test_generate_diff_plain']['expect'])
    result = result.split('\n')
    result = set(map(lambda line: line.strip(), result))
    assert result == expect


def test_generate_diff_json(tree_first_json, tree_second_json):
    data1 = file_parser.get_data(tree_first_json)
    data2 = file_parser.get_data(tree_second_json)
    expect = evaluator.get_diff(data1, data2)
    result = evaluator.generate_diff(
        tree_first_json, tree_second_json, 'json'
    )
    assert json.loads(result) == expect


def test_generate_diff_json_yaml(tree_first_yaml, tree_second_yaml):
    data1 = file_parser.get_data(tree_first_yaml)
    data2 = file_parser.get_data(tree_second_yaml)
    expect = evaluator.get_diff(data1, data2)
    result = evaluator.generate_diff(
        tree_first_yaml, tree_second_yaml, 'json'
    )
    assert json.loads(result) == expect
