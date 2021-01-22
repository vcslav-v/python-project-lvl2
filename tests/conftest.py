"""Test json fixtures."""
import pytest
import os

fixtures_path = os.path.join('tests', 'fixtures')


@pytest.fixture
def tree_first_json():
    return os.path.join(fixtures_path, 'tree_first.json')


@pytest.fixture
def tree_second_json():
    return os.path.join(fixtures_path, 'tree_second.json')


@pytest.fixture
def wrong_json():
    return os.path.join(fixtures_path, 'wrong.json')


@pytest.fixture
def fake_json(tmp_path):
    json_file = tmp_path / 'fake.json'
    return json_file


@pytest.fixture
def tree_first_yaml():
    return os.path.join(fixtures_path, 'tree_first.yaml')


@pytest.fixture
def tree_second_yaml():
    return os.path.join(fixtures_path, 'tree_second.yaml')


@pytest.fixture
def wrong_yaml():
    return os.path.join(fixtures_path, 'wrong.yaml')


@pytest.fixture
def fake_yaml(tmp_path):
    yaml_file = tmp_path / 'fake.yaml'
    return yaml_file


@pytest.fixture
def toml_format():
    return os.path.join(fixtures_path, 'file.toml')
