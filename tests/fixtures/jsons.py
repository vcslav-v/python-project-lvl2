"""Test json fixtures."""
import pytest


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
