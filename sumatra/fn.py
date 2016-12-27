import types
import inspect
from functools import wraps

import requests
import json

from sumatra import client, errors


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


def fn(remote_only=True):
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
      function = parse(fn)
      try:
        return call(function)
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
  (app_name, app_token) = client.data()
  if app_name is None or app_token is None:
    raise errors.CredentialsError()
  (protocol, host, port) = client.server()
  url_keys = '%s://%s.%s:%s'
  url_values = (protocol, app_name, host, port)
  url = url_keys % url_values
  headers = {
    'Authentication': 'Bearer %s' % app_token,
    'Content-Type': 'application/json'
  }
  try:
    req = requests.post(url, data=json.dumps(data), headers=headers)
  except requests.exceptions.ConnectionError:
    raise errors.ServiceReachError(url)
  try:
    res = req.json()
  except json.decoder.JSONDecodeError:
    raise errors.ResponseFormatError(req.text)
  if 'error' in res:
    raise errors.FunctionError(res['error'])
  return res['result']
  
