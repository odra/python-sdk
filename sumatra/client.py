import json
import os

import yaml

from sumatra import errors

_app_name = None
_app_token = None
_protocol = 'http'
_host = 'fn.sumatra.io'
_port =  80


def bootstrap(name=None, token=None, file=None, **kwargs):
  """
  Bootstraps the client with a name, token and server data to access the remote server.
  
  param: name(str) -  the remote application name
  param: token(str) - the token be used to access the remote application
  param: procotol(str) - sets the request protocol, only supports http or https
  param: host(str) - the server hostname to be used when creating the request
  param: port(int) - the server port to use
  """
  bootstrap_server(**kwargs)
  if file is not None:
    bootstrap_from_file(file)
    return
  bootstrap_app(name, token)


def bootstrap_server(protocol='http', host='fn.sumatra.io', port=80):
  """
  bootstraps the server properties

  param: procotol(str) - sets the request protocol, only supports http or https
  param: host(str) - the server hostname to be used when creating the request
  param: port(int) - the server port to use
  """
  global _protocol
  global _host
  global _port
  (_protocol, _host, _port) = (protocol, host, port)


def bootstrap_app(name, token):
  """
  bootstraps the application data (name and token) to use on each request

  param: name(str) - application name
  param: token(str) - application secret token
  """
  global _app_name
  global _app_token
  (_app_name, _app_token) = (name, token)


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
    (app, token) = (cfg.get('name'), cfg.get('token'))
    bootstrap_server(**server)
    bootstrap_app(app, token)


def data():
  """
  Gets the client application name and token in a tuple.

  Returns:
    A tuple containing the application name and token.
  """
  return (_app_name, _app_token)


def server():
  """
  Gets the client server information

  Returns:
    A tuple containing the application protocol, hostname and port
  """
  return (_protocol, _host, _port)


def reset():
  """
  Resets the application name and token (sets both to None).
  """
  global _app_name
  global _app_token
  (_app_name, _app_token) = (None, None)
