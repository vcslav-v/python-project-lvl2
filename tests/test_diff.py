"""Tests for gendiff"""
import json
import os

import pytest
from gendiff import evaluator, file_parser

expect_files_path = os.path.join('tests', 'expects')


@pytest.mark.parametrize('style_format, expect_file', [
    ('stylish', 'generate_diff_stylish.txt'),
    ('plain', 'generate_diff_plain.txt')
])
def test_generate_diff_formats(
    tree_first_json,
    tree_second_json,
    style_format,
    expect_file
):
    result = evaluator.generate_diff(
        tree_first_json, tree_second_json, style_format
    )
    with open(
        os.path.join(expect_files_path, expect_file), 'r'
    ) as expect_file:
        expect = expect_file.read()
    assert result == expect


@pytest.mark.parametrize('start_file, end_file', [
    ('tree_first_json', 'tree_second_json'),
    ('tree_first_yaml', 'tree_first_yaml')
])
def test_generate_diff_json(start_file, end_file, request):
    start_file = request.getfixturevalue(start_file)
    end_file = request.getfixturevalue(end_file)

    data1 = file_parser.get_data(start_file)
    data2 = file_parser.get_data(end_file)
    expect = evaluator.get_diff(data1, data2)
    result = evaluator.generate_diff(
        start_file, end_file, 'json'
    )
    assert json.loads(result) == expect
