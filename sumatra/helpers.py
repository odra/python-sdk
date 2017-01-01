import json
import inspect


BYTES_PROPS = ('code', 'lnotab')


def get_fn_name(fn):
  """
  Gets the function full name (full module path + name)

  param: fn(Function) - A function to be inspected

  Returns:
    A string containing the full function name + module(s)
  """
  module = inspect.getmodule(fn).__name__
  return '%s.%s' % (module, fn.__name__)


def is_code_prop(prop):
  """
  Checks if property name is a code property (checks if it starts with "co_").

  param: prop(str) - property name string

  Returns:
    A bool indicating if it is a code property or not.
  """
  return prop.startswith('co_')


def clean_code_prop(prop):
  """
  Clean code object property by removing the "co_" preffix.

  param: prop(str) - string property name

  Returns:
    A string with the new property name.
  """
  if is_code_prop(prop) is False:
    return prop
  return prop.replace('co_', '')


def code_to_dict(fn):
  """
  Retrieves the code object properies from a function and returns it in a dict.

  param: fn(Function) - a function object 

  Returns:
    A dict with the function code object properties.
  """
  spec = inspect.getargspec(fn)
  code = fn.__code__
  props = dir(code)
  data = {clean_code_prop(k):getattr(code, k) for k in props if is_code_prop(k)}
  if spec.defaults:
    data['defaults'] = spec.defaults
  return data


def code_encode_json_hook(obj):
  """
  JSON object_hook to parse dict bytes to string so it can be transformed into a json string.

  param: obj(dict) - Dict to be transformed into a json string (code object dict).

  Returns:
    A dict with the proper field conversion.
  """
  for (k, v) in obj.items():
    if type(v) is bytes:
      obj[k] = v.decode('utf8')
  return obj


def code_decode_json_hook(obj):
  """
  JSON object_hook to decode jsonstring into dicts for code objects.

  param: obj(dict) - dict to be used by the json object_hook.

  Returns:
    A dict with the proper converted fields.
  """
  for (k, v) in obj.items():
    if type(v) is str and k in BYTES_PROPS:
      obj[k] = v.encode('utf8')
    if type(v) is list:
      obj[k] = tuple(v)
  return obj


def code_to_json(fn):
  """
  Simple wrapper that parses function code object into jsonstring data.

  param: fn(Function) - Function object to be used.

  Returns:
    A json data string with function code object information.
  """
  data = code_to_dict(fn)
  data = code_encode_json_hook(data)
  return json.dumps(data)


def json_to_code(jsonstring):
  """
  Parses a json string into a code object.

  param: jsonstring(str) - JSON string to be parsed.

  Returns:
    A dict with the proper code object values.
  """
  return json.loads(jsonstring, object_hook=code_decode_json_hook)


def encode_body(s, encoding='utf8'):
  """
  Encodes a string in a base64 one.

  param: s(str) - The string to be encoded.
  param: encoding(str) - Encoding to be used, default is utf-8

  Returns:
    A base64 encoded string.
  """
  return base64.encode(s.encode(encode))
