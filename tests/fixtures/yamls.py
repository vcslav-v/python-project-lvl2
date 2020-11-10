"""Test json fixtures."""
import pytest


@pytest.fixture
def first_yaml(tmp_path):
    content = """host: hexlet.io
timeout: 50
proxy: 123.234.53.22
follow: false
    """
    yaml_file = tmp_path / 'first.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def second_yaml(tmp_path):
    content = """timeout: 20
verbose: true
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
