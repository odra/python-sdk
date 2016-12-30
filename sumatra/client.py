import json
import os

import yaml

from sumatra import errors, dockerengine


_url = None
_encoding = None


def bootstrap(url='unix://var/run/docker.sock', encoding='utf8', file=None):
  """
  Bootstraps the client with a name, token and server data to access the remote server.
  
  param: name(str) -  the remote application name
  param: token(str) - the token be used to access the remote application
  param: procotol(str) - sets the request protocol, only supports http or https
  param: host(str) - the server hostname to be used when creating the request
  param: port(int) - the server port to use
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
  Gets the client application name and token in a tuple.

  Returns:
    A tuple containing the application name and token.
  """
  return (_url, _encoding)


def reset():
  """
  Resets the application name and token (sets both to None).
  """
  global _url
  global _encoding
  (_url, _encoding) = (None, None)
