"""Test json fixtures."""
import pytest
import os
import csv

with open(
    os.path.join('tests', 'fixtures', 'fixture_content.csv'), 'r'
) as fixture_content_file:
    fixture_content = csv.reader(fixture_content_file)
    fixture_content = dict(fixture_content)


@pytest.fixture
def flat_first_yaml(tmp_path):
    content = fixture_content['flat_first_yaml']
    yaml_file = tmp_path / 'first.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def flat_second_yaml(tmp_path):
    content = fixture_content['flat_second_yaml']
    yaml_file = tmp_path / 'second.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def tree_first_yaml(tmp_path):
    content = fixture_content['tree_first_yaml']
    yaml_file = tmp_path / 'tree_first.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def tree_second_yaml(tmp_path):
    content = fixture_content['tree_second_yaml']
    yaml_file = tmp_path / 'tree_second.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def wrong_yaml(tmp_path):
    content = fixture_content['wrong_yaml']
    yaml_file = tmp_path / 'wrong.yaml'
    yaml_file.write_text(content)
    return yaml_file


@pytest.fixture
def fake_yaml(tmp_path):
    yaml_file = tmp_path / 'fake.yaml'
    return yaml_file
