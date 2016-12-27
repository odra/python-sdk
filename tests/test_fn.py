import inspect

import pytest
import requests
import requests_mock
import json

import sumatra
from sumatra import fn, client, errors


@pytest.fixture
def func1():
  def _fn(x, y=2):
    return (x, y + 3)
  return _fn


@pytest.fixture
def code(func1):
  return func1.__code__


@pytest.fixture
def mock_func():
  @sumatra.function()
  def x():
    return 1
  return x


@pytest.fixture
def mock_func1():
  @sumatra.function(remote_only=False)
  def x():
    return 1
  return x


@pytest.fixture
def bootstrap():
  client.bootstrap('myapp', '12345', protocol='https')


def test_parse_function(func1, code):
  data = fn.parse(func1)
  props = [prop for prop in dir(code) if prop.startswith('co_')]
  for prop in props:
    value = getattr(code, prop)
    if type(value) is bytes:
      value = value.decode('utf-8')
    assert data[prop] == value  


def test_decorator(mock_func, bootstrap):
  mock_res = {
    'jsonrpc': '2.0',
    'id': 1,
    'result': 1
  }
  with requests_mock.mock() as m:
    m.post('https://myapp.fn.sumatra.io:80', json=mock_res, status_code=201)
    res = mock_func()
    assert res == 1

def test_decorator_connection_error(bootstrap, mock_func):
  with pytest.raises(errors.ServiceReachError):
    mock_func()


def test_decorator_bootstrap_error(mock_func):
  client.reset()
  with pytest.raises(errors.CredentialsError):
    mock_func()


def test_decorator_json_error(bootstrap): 
  @sumatra.function()
  def x():
    return 1
  with requests_mock.mock() as m:
    m.post('https://myapp.fn.sumatra.io:80', text='aaa', status_code=201)
    with pytest.raises(errors.ResponseFormatError):
      x()


def test_decorator_error_function(mock_func, bootstrap):
  mock_res = {
    'jsonrpc': '2.0',
    'id': 1,
    'error': {
      'code': 1,
      'message': 'Function took too long to process.',
      'data': None
    }
  }
  with requests_mock.mock() as m:
    m.post('https://myapp.fn.sumatra.io:80', json=mock_res, status_code=201)
    with pytest.raises(errors.FunctionError):
      mock_func()
