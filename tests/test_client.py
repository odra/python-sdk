import os

import pytest

from sumatra import client, errors


current_dir = os.path.dirname(os.path.realpath(__file__))
yaml_file = '%s/fixtures/.sumatra.yaml' % current_dir


@pytest.fixture
def bootstrap():
  client.bootstrap('name', 'token')


@pytest.fixture
def reset():
  client.reset()


def test_empty_vars():
  (name, token)  = client.data()
  assert name is None
  assert token is None 


def test_vars(bootstrap):
  (name, token)  = client.data()
  assert name == 'name'
  assert token == 'token' 


def test_vars_again():
  (name, token)  = client.data()
  assert name == 'name'
  assert token == 'token'


def test_clean():
  client.reset()
  (name, token)  = client.data()
  assert name is None
  assert token is None


def test_file_path(reset):
  client.bootstrap(file=yaml_file)
  (name, token)  = client.data()
  assert name == 'myapp'
  assert token == '12345'


def test_file_path_json(reset):
  client.bootstrap(file=yaml_file.replace('.yaml', '.json'))
  (name, token)  = client.data()
  assert name == 'myapp'
  assert token == '12345'


def test_invalid_file_path(reset):
  with pytest.raises(errors.ConfigFilePathError):
    client.bootstrap(file=yaml_file.replace('.yaml', ''))


def test_invalid_file(reset):
  with pytest.raises(errors.ConfigFileParseError):
    client.bootstrap(file=yaml_file.replace('.yaml', '-invalid.yaml'))
