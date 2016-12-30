import os

import pytest

from sumatra import client, errors


current_dir = os.path.dirname(os.path.realpath(__file__))
yaml_file = '%s/fixtures/.sumatra.yaml' % current_dir


@pytest.fixture
def bootstrap():
  client.bootstrap('unix://var/run/docker.sock', 'utf8')


@pytest.fixture
def reset():
  client.reset()


def test_empty_vars():
  (url, encoding)  = client.data()
  assert url is None
  assert encoding is None 


def test_vars(bootstrap):
  (url, encoding)  = client.data()
  assert url == 'unix://var/run/docker.sock'
  assert encoding == 'utf8' 


def test_vars_again():
  (url, encoding)  = client.data()
  assert url == 'unix://var/run/docker.sock'
  assert encoding == 'utf8'


def test_clean():
  client.reset()
  (url, encoding)  = client.data()
  assert url is None
  assert encoding is None


def test_file_path(reset):
  client.bootstrap(file=yaml_file)
  (url, encoding)  = client.data()
  assert url == 'unix://var/run/docker.sock'
  assert encoding == 'utf8'


def test_file_path_json(reset):
  client.bootstrap(file=yaml_file.replace('.yaml', '.json'))
  (url, encoding)  = client.data()
  assert url == 'unix://var/run/docker.sock'
  assert encoding == 'utf8'


def test_invalid_file_path(reset):
  with pytest.raises(errors.ConfigFilePathError):
    client.bootstrap(file=yaml_file.replace('.yaml', ''))


def test_invalid_file(reset):
  with pytest.raises(errors.ConfigFileParseError):
    client.bootstrap(file=yaml_file.replace('.yaml', '-invalid.yaml'))
