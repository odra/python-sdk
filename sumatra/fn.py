import types
import inspect
from functools import wraps

import requests
import json

from sumatra import client, errors, helpers, dockerengine


def parse(func):
  """
  Reads and parses function data to send it to the server.

  param: func(function) - a function to be parsed
  """
  module = inspect.getmodule(func)
  data = {
    'namespace': module.__name__
  }
  byte_code = func.__code__
  props = [prop for prop in dir(byte_code) if prop.startswith('co_')]
  for prop in props:
    value = getattr(byte_code, prop)
    if type(value) is bytes:
      value = value.decode('utf-8')
    data[prop] = value
  spec = inspect.getargspec(func)
  data['arg_spec'] = {
    'args': spec.args,
    'varargs': spec.varargs,
    'keywords': spec.keywords,
    'defaults': spec.defaults
  }
  return data


def fn(remote_only=True, platform='python-2.7'):
  """
  Decorator to speicify a function to be run in the remote server.

  If the function does not exist or is different from the one stored in the server,
  the platform will create/update the function code and run it 
  (first time might be slower due to creation or changes).

  param: remote_only(bool) - false value runs locally if the client fails to connect to the server (default is True) 
  """
  def decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      try:
        return call(fn)
      except errors.ServiceReachError as e:
        if remote_only is False:
          return fn(*args, **kwargs)
        raise e
    return wrapper
  return decorator


def call(data):
  """
  Executes a post http request to the platform.

  param: data(dict) - a dictionary to be sent as a json string in the request

  Returns:
    A dict with the parsed json
  """
  output = dockerengine.run('random-name', data=data)
  result = json.loads(output.decode('utf8'))
  if 'error' in result:
    raise errors.FunctionError(result['error'])
  return result['result']  
