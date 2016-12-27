import json


class BaseError(Exception):
  """
  Base error class to be used by other error classes.
  """
  def __init__(self, code=None, message=None, data=None):
    """
    param: code(int) - A unique error code
    param: message(str) - A human explanation of the error
    param: data - A dict containing useful data about the error 
    """
    self.code = code
    self.message = message
    self.data = data

  def __repr__(self):
    return '%s(%s)' % (self.__class__.__name__, self.code)

  def as_dict(self):
    """
    Python dict representation of the error.

    Returns:
      A dictionary containing the error code, message and data
    """
    data = {
      'code': self.code,
      'message': self.message,
      'error': self.data
    }
    return data

  def as_json(self):
    """
    JSON string representation of the error. It uses the as_dict() method.

    Returns:
      A string contaning the result of as_dict() as a json string.
    """
    return  json.dumps(self.as_dict())


class CredentialsError(BaseError):
  """
  Raised when trying to execute a request when the client was
  not properly bootstraped (no application name and token). 
  """
  def __init__(self, *args, **kwargs):
    super(CredentialsError, self).__init__(*args, **kwargs)
    self.code = -32000
    self.message = 'Local credentials not set properly.'


class ConfigFilePathError(BaseError):
  """
  Raised when the bootstrap method can't find the config file.
  """
  def __init__(self, path, *args, **kwargs):
    super(ConfigFilePathError, self).__init__(*args, **kwargs)
    self.code = -32001
    self.path = path
    self.message = 'Config file not found in path: %s' % path 


class ConfigFileParseError(BaseError):
  """
  Raised when the bootstrap method can't parse the config file as a yaml or
  json file.
  """
  def __init__(self, path, *args, **kwargs):
    super(ConfigFileParseError, self).__init__(*args, **kwargs)
    self.code = -32001
    self.path = path
    self.message = 'Invalid yaml format: %s' % path


class ServiceReachError(BaseError):
  def __init__(self, url, *args, **kwargs):
    super(ServiceReachError, self).__init__(*args, **kwargs)
    self.code = -32002
    self.url = url
    self.message = 'Could not reach service on url: %s' % url


class ResponseFormatError(BaseError):
  def __init__(self, text, *args, **kwargs):
    super(ResponseFormatError, self).__init__(*args, **kwargs)
    self.code = -32003
    self.text = text
    self.message = 'Invalid response format: %s' % text

class FunctionError(BaseError):
  def __init__(self, error, *args, **kwargs):
    super(FunctionError, self).__init__(*args, **kwargs)
    self.code = -32004
    self.message = error['message']
    self.data = error['data']
    self.error_code = error['code']
