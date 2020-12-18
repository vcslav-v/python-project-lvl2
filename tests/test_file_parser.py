"""Tests for file parser"""
import json
import yaml
import os

import pytest

from differences_evaluator import file_parser
from tests.fixtures.jsons import first_json, wrong_json, fake_json
from tests.fixtures.yamls import first_yaml, wrong_yaml, fake_yaml

with open(
    os.path.join('tests', 'fixtures', 'expect.json'), 'r'
) as expects:
    expects = json.load(expects)


def test_get_extension_simple_file():
    result = file_parser.get_extension(
        'file_name.json'
    )
    assert (result == 'json')


def test_get_extension_unix_file_path():
    result = file_parser.get_extension(
        '/Users/user/Downloads/file_name.yaml'
    )
    assert (result == 'yaml')


def test_get_extension_win_file_path():
    result = file_parser.get_extension(
        r'C:\\Downloads\file_name.png'
    )
    assert (result == 'png')


def test_get_extension_many_dots():
    result = file_parser.get_extension(
        'file.name.exe'
    )
    assert (result == 'exe')


def test_get_data_many_dots():
    result = file_parser.get_extension(
        'file.name.exe'
    )
    assert (result == 'exe')


def test_get_data_json(first_json):
    result = file_parser.get_data(first_json)
    assert (result == expects['test_get_data_json'])


def test_get_data_json_wrong_json(wrong_json):
    with pytest.raises(json.JSONDecodeError):
        file_parser.get_data(wrong_json)


def test_get_data_json_fake_json(fake_json):
    with pytest.raises(FileNotFoundError):
        file_parser.get_data(fake_json)


def test_get_data_yaml(first_yaml):
    result = file_parser.get_data(first_yaml)
    assert (result == expects['test_get_data_json'])


def test_get_data_json_wrong_yaml(wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        file_parser.get_data(wrong_yaml)


def test_get_data_json_fake_yaml(fake_yaml):
    with pytest.raises(FileNotFoundError):
        file_parser.get_data(fake_yaml)
