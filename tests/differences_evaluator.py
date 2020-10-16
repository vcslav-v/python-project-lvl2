"""Tests for differences_evaluator"""
from json import JSONDecodeError

import pytest

from differences_evaluator import evaluator


@pytest.fixture
def first_json(tmp_path):
    content = """{
        "host": "hexlet.io",
        "timeout": 50,
        "proxy": "123.234.53.22",
        "follow": false
    }
    """
    json_file = tmp_path / 'first.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def second_json(tmp_path):
    content = """{
        "timeout": 20,
        "verbose": true,
        "host": "hexlet.io"
    }
    """
    json_file = tmp_path / 'second.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def wrong_json(tmp_path):
    content = """{
        "timeout: 20
    }
    """
    json_file = tmp_path / 'wrong.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def fake_json(tmp_path):
    json_file = tmp_path / 'fake.json'
    return json_file


def test_format_generate_diff(first_json, second_json):
    result = evaluator.generate_diff(first_json, second_json)
    assert (result[0], result[-1]) == ('{', '}')


def test_values_generate_diff(first_json, second_json):
    expect = {
        '- follow: False',
        'host: hexlet.io',
        '- proxy: 123.234.53.22',
        '- timeout: 50',
        '+ timeout: 20',
        '+ verbose: True',
    }
    result = evaluator.generate_diff(first_json, second_json)
    result = result.split('\n')
    result = list(map(lambda line: line.strip(), result))
    result = set(result[1:-1])
    assert result == expect


def test_wrong_json_exceptions_json_generate_diff(first_json, wrong_json):
    with pytest.raises(JSONDecodeError):
        evaluator.generate_diff(first_json, wrong_json)


def test_not_exist_exceptions_json_generate_diff(first_json, fake_json):
    with pytest.raises(FileNotFoundError):
        evaluator.generate_diff(first_json, fake_json)
