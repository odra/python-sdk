import pytest
import json

from sumatra import dockerengine, helpers


@pytest.fixture
def func():
  def fn():
    return 'Hello World'
  return fn


def test_run(func):
  code = helpers.code_to_dict(func)
  cmd = dockerengine.run('forest', data=func)
  cmd = json.loads(cmd.decode('utf8'))
  assert cmd['result'] == 'Hello World'
