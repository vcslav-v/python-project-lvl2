"""Tests for file parser"""
import json
import yaml

import pytest

from gendiff import file_parser


def test_get_data_json(flat_first_json):
    result = file_parser.get_data(flat_first_json)
    expect = {
        'host': 'hexlet.io',
        'timeout': 50,
        'proxy': '123.234.53.22',
        'follow': False
    }
    assert (result == expect)


def test_get_data_json_wrong_json(wrong_json):
    with pytest.raises(json.JSONDecodeError):
        file_parser.get_data(wrong_json)


def test_get_data_json_fake_json(fake_json):
    with pytest.raises(FileNotFoundError):
        file_parser.get_data(fake_json)


def test_get_data_yaml(flat_first_yaml):
    result = file_parser.get_data(flat_first_yaml)
    expect = {
        'test': 'some_string',
        'num': 43,
        'ip_address': '192.168.1.1',
        'boolean': False
    }
    assert (result == expect)


def test_get_data_json_wrong_yaml(wrong_yaml):
    with pytest.raises(yaml.scanner.ScannerError):
        file_parser.get_data(wrong_yaml)


def test_get_data_json_fake_yaml(fake_yaml):
    with pytest.raises(FileNotFoundError):
        file_parser.get_data(fake_yaml)
