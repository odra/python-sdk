import json

import pytest

from sumatra import helpers


@pytest.fixture
def func():
  def fn():
    return 'Hello World'
  return fn


def test_is_code_prop_true():
  assert helpers.is_code_prop('co_code') is True


def test_is_code_prop_false():
  assert helpers.is_code_prop('code') is False  


def test_clean_code_prop():
  assert helpers.clean_code_prop('co_code') == 'code'


def test_clean_code_prop_invalid():
  assert helpers.clean_code_prop('codeco_') == 'codeco_'


def test_code_to_dict(func):
  data = helpers.code_to_dict(func)
  for (k, v) in data.items():
    assert v == getattr(func.__code__, 'co_%s' % k)


def test_code_to_json(func):
  data = helpers.code_to_json(func)
  data = helpers.json_to_code(data)
  for (k, v) in data.items():
    prop = getattr(func.__code__, 'co_%s' % k)
    assert v == getattr(func.__code__, 'co_%s' % k)
