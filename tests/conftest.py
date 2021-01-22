"""Test json fixtures."""
import pytest
import os

fixtures_path = os.path.join('tests', 'fixtures')


@pytest.fixture
def flat_first_json(tmp_path):
    with open(
        os.path.join(fixtures_path, 'flat_first.json'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    json_file = tmp_path / 'first.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def flat_second_json(tmp_path):
    with open(
        os.path.join(fixtures_path, 'flat_second.json'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    json_file = tmp_path / 'second.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def tree_first_json(tmp_path):
    with open(
        os.path.join(fixtures_path, 'tree_first.json'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    json_file = tmp_path / 'tree_first.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def tree_second_json(tmp_path):
    with open(
        os.path.join(fixtures_path, 'tree_second.json'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    json_file = tmp_path / 'tree_second.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def wrong_json(tmp_path):
    with open(
        os.path.join(fixtures_path, 'wrong.json'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    json_file = tmp_path / 'wrong.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def fake_json(tmp_path):
    json_file = tmp_path / 'fake.json'
    return json_file


@pytest.fixture
def flat_first_yaml(tmp_path):
    with open(
        os.path.join(fixtures_path, 'flat_first.yaml'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    yaml_file = tmp_path / 'first.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def flat_second_yaml(tmp_path):
    with open(
        os.path.join(fixtures_path, 'flat_second.yaml'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    yaml_file = tmp_path / 'second.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def tree_first_yaml(tmp_path):
    with open(
        os.path.join(fixtures_path, 'tree_first.yaml'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    yaml_file = tmp_path / 'tree_first.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def tree_second_yaml(tmp_path):
    with open(
        os.path.join(fixtures_path, 'tree_second.yaml'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    yaml_file = tmp_path / 'tree_second.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def wrong_yaml(tmp_path):
    with open(
        os.path.join(fixtures_path, 'wrong.yaml'), 'r'
    ) as fixture_file:
        content = ''.join(fixture_file.readlines())
    yaml_file = tmp_path / 'wrong.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def fake_yaml(tmp_path):
    yaml_file = tmp_path / 'fake.yaml'
    return yaml_file
