import json
import os

import yaml

from sumatra import errors, dockerengine


_url = None
_encoding = None


def bootstrap(url='unix://var/run/docker.sock', encoding='utf8', file=None):
  """
  Bootstraps the client with a name, token and server data to access the remote server.
  
  param: url(str) -  the remote application url
  param: encoding(str) - the encoding to be used by several parts of the application, default is utf-8
  param: file(str) - file config path to be used (json or yaml) instead of hardcoded config.
  """
  global _url
  global _encoding
  _url = url
  _encoding = encoding
  if file is not None:
    return bootstrap_from_file(file)
  return dockerengine.bootstrap(url)


def bootstrap_from_file(path):
  """
  bootstraps application and server info from a yaml/json file

  param: path(str) - file path to read and parse
  """
  if os.path.exists(path) is False:
    raise errors.ConfigFilePathError(path)
  with open(path) as f:
    try:
      cfg = yaml.load(f)
    except yaml.YAMLError:
      raise errors.ConfigFileParseError(path)
    cfg = cfg.get('sumatra')
    server = cfg.get('server', {})
    bootstrap(**server)


def data():
  """
  Gets the client application url and encoding in a tuple.

  Returns:
    A tuple containing the application url and encoding.
  """
  return (_url, _encoding)


def reset():
  """
  Resets the application url and encoding (sets both to None).
  """
  global _url
  global _encoding
  (_url, _encoding) = (None, None)
