"""Test json fixtures."""
import pytest
import csv
import os


with open(
    os.path.join('tests', 'fixtures', 'fixture_content.csv'), 'r'
) as fixture_content_file:
    fixture_content = csv.reader(fixture_content_file)
    fixture_content = dict(fixture_content)


@pytest.fixture
def flat_first_json(tmp_path):
    content = fixture_content['flat_first_json']
    json_file = tmp_path / 'first.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def flat_second_json(tmp_path):
    content = fixture_content['flat_second_json']
    json_file = tmp_path / 'second.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def tree_first_json(tmp_path):
    content = fixture_content['tree_first_json']
    json_file = tmp_path / 'tree_first.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def tree_second_json(tmp_path):
    content = fixture_content['tree_second_json']
    json_file = tmp_path / 'tree_second.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def wrong_json(tmp_path):
    content = fixture_content['wrong_json']
    json_file = tmp_path / 'wrong.json'
    json_file.write_text(content)
    return json_file


@pytest.fixture
def fake_json(tmp_path):
    json_file = tmp_path / 'fake.json'
    return json_file
