"""Tests for formaters"""
import json
import os

from differences_evaluator import formaters

with open(
    os.path.join('tests', 'fixtures', 'formaters_content.json'), 'r'
) as test_content_file:
    test_content = json.load(test_content_file)


def test_stylish():
    result = formaters.stylish(
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
    result = formaters.stylish(
        *test_content['test_stylish_empty_diff']['args']
    )
    assert result == test_content['test_stylish_empty_diff']['expect']


def test_plain():
    result = formaters.plain(
        *test_content['test_plain']['args']
    )
    expect = set(test_content['test_plain']['expect'])
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    result = set(result)
    assert result == expect


def test_plain_empty_diff():
    result = formaters.plain(
        *test_content['test_plain_empty_diff']['args']
    )
    assert result == test_content['test_plain_empty_diff']['expect']


def test_json_diff_formater():
    result = json.loads(formaters.json_diff_formater(
        *test_content['test_json_diff_formater']['args']
    ))
    expect = test_content['test_json_diff_formater']['expect']
    assert result == expect


def test_json_diff_formater_empty_diff():
    result = json.loads(formaters.json_diff_formater(
        *test_content['test_json_diff_formater_empty_diff']['args']
    ))
    assert result == (
        test_content['test_json_diff_formater_empty_diff']['expect']
        )
