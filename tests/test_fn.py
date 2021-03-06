import inspect

import pytest
import requests
import requests_mock
import json

import sumatra
from sumatra import fn, client, errors

@pytest.fixture
def func():
  @sumatra.function()
  def x():
    return 1
  return x


@pytest.fixture
def bootstrap():
  client.bootstrap('unix://var/run/docker.sock', 'utf8')


def test_decorator(func, bootstrap):
  assert func() == 1
