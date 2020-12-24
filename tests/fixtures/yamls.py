"""Test json fixtures."""
import pytest


@pytest.fixture
def first_yaml(tmp_path):
    content = """test: some_string
num: 43
ip_address: 192.168.1.1
boolean: false
    """
    yaml_file = tmp_path / 'first.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def second_yaml(tmp_path):
    content = """ip_address: 255.255.1.1
boolean: false
host: hexlet.io
    """
    yaml_file = tmp_path / 'second.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def wrong_yaml(tmp_path):
    content = """timeout 20
verbose: true
host: hexlet.io
    """
    yaml_file = tmp_path / 'wrong.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def fake_yaml(tmp_path):
    yaml_file = tmp_path / 'fake.yaml'
    return yaml_file
