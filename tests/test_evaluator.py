"""Tests for differences_evaluator"""
import json
import os

from differences_evaluator import evaluator, file_parser

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


def test_get_diff_flat_json(flat_first_json, flat_second_json):
    start_data = file_parser.get_data(flat_first_json)
    end_data = file_parser.get_data(flat_second_json)
    result = evaluator.get_diff(start_data, end_data)
    print(result)
    for leaf in result['leafs']:
        assert leaf in (
            test_content['test_get_diff_flat_json']['expect']['leafs']
        )
    result['leafs'] = (
        test_content['test_get_diff_flat_json']['expect']['leafs']
        )
    assert result == test_content['test_get_diff_flat_json']['expect']


def test_get_diff_flat_yaml(flat_first_yaml, flat_second_yaml):
    start_data = file_parser.get_data(flat_first_yaml)
    end_data = file_parser.get_data(flat_second_yaml)
    result = evaluator.get_diff(start_data, end_data)
    for leaf in result['leafs']:
        assert leaf in (
            test_content['test_get_diff_flat_yaml']['expect']['leafs']
            )
    result['leafs'] = (
        test_content['test_get_diff_flat_yaml']['expect']['leafs']
    )
    assert result == test_content['test_get_diff_flat_yaml']['expect']


def test_get_diff_tree_json(tree_first_json, tree_second_json):
    start_data = file_parser.get_data(tree_first_json)
    end_data = file_parser.get_data(tree_second_json)
    result = evaluator.get_diff(start_data, end_data)
    compare_node(
        result,
        test_content['test_get_diff_tree_json']['expect']
    )


def test_get_diff_tree_yaml(tree_first_yaml, tree_second_yaml):
    start_data = file_parser.get_data(tree_first_yaml)
    end_data = file_parser.get_data(tree_second_yaml)
    result = evaluator.get_diff(start_data, end_data)
    compare_node(
        result,
        test_content['test_get_diff_tree_yaml']['expect']
    )


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
    result = evaluator.generate_diff(
        tree_first_json, tree_second_json, 'json'
        )
    result = json.loads(result)
    compare_node(result, test_content['test_generate_diff_json']['expect'])


def test_generate_diff_json_yaml(tree_first_yaml, tree_second_yaml):
    result = evaluator.generate_diff(
        tree_first_yaml, tree_second_yaml, 'json'
        )
    result = json.loads(result)
    compare_node(
        result, test_content['test_generate_diff_json_yaml']['expect']
        )
