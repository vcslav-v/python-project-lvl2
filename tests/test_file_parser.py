"""Tests for file parser"""
import json
import yaml
import os

import pytest

from differences_evaluator import file_parser

with open(
    os.path.join('tests', 'fixtures', 'file_parser_content.json'), 'r'
) as test_content_file:
    test_content = json.load(test_content_file)


def test_get_data_json(flat_first_json):
    result = file_parser.get_data(flat_first_json)
    expect = test_content['test_get_data_json']['expect']
    assert (result == expect)


def test_get_data_json_wrong_json(wrong_json):
    with pytest.raises(json.JSONDecodeError):
        file_parser.get_data(wrong_json)


def test_get_data_json_fake_json(fake_json):
    with pytest.raises(FileNotFoundError):
        file_parser.get_data(fake_json)


def test_get_data_yaml(flat_first_yaml):
    result = file_parser.get_data(flat_first_yaml)
    expect = test_content['test_get_data_yaml']['expect']
    assert (result == expect)


def test_get_data_json_wrong_yaml(wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        file_parser.get_data(wrong_yaml)


def test_get_data_json_fake_yaml(fake_yaml):
    with pytest.raises(FileNotFoundError):
        file_parser.get_data(fake_yaml)
