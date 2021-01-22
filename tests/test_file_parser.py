"""Tests for file parser"""
import json
import yaml

import pytest

from gendiff import file_parser


@pytest.mark.parametrize('data_file, load_func', [
    ('tree_first_json', json.load),
    ('tree_first_yaml', lambda x: yaml.load(x, Loader=yaml.FullLoader))
])
def test_get_data(data_file, load_func, request):
    data_file = request.getfixturevalue(data_file)
    result = file_parser.get_data(data_file)
    with open(data_file) as open_file:
        expect = load_func(open_file)
    assert (result == expect)


@pytest.mark.parametrize('problem_file, error_type', [
    ('wrong_json', json.JSONDecodeError),
    ('wrong_yaml', yaml.scanner.ScannerError),
    ('fake_json', FileNotFoundError),
    ('fake_yaml', FileNotFoundError),
    ('toml_format', ValueError)
])
def test_get_data_wrong(problem_file, error_type, request):
    problem_file = request.getfixturevalue(problem_file)
    with pytest.raises(error_type):
        file_parser.get_data(problem_file)
