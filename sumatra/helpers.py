import json
import inspect


BYTES_PROPS = ('code', 'lnotab')


def get_fn_name(fn):
  module = inspect.getmodule(fn).__name__
  return '%s.%s' % (module, fn.__name__)


def is_code_prop(prop):
  if 'kwonlyargcount' in prop:
    return False
  return prop.startswith('co_')


def clean_code_prop(prop):
  if is_code_prop(prop) is False:
    return prop
  return prop.replace('co_', '')


def code_to_dict(fn):
  spec = inspect.getargspec(fn)
  code = fn.__code__
  props = dir(code)
  data = {clean_code_prop(k):getattr(code, k) for k in props if is_code_prop(k)}
  if spec.defaults:
    data['defaults'] = spec.defaults
  return data


def code_encode_json_hook(obj):
  for (k, v) in obj.items():
    if type(v) is bytes:
      obj[k] = v.decode('utf8')
  return obj


def code_decode_json_hook(obj):
  for (k, v) in obj.items():
    if type(v) is str and k in BYTES_PROPS:
      obj[k] = v.encode('utf8')
    if type(v) is list:
      obj[k] = tuple(v)
  return obj


def code_to_json(fn):
  data = code_to_dict(fn)
  data = code_encode_json_hook(data)
  return json.dumps(data)


def json_to_code(jsonstring):
  return json.loads(jsonstring, object_hook=code_decode_json_hook)


def encode_body(s, encoding='utf8'):
  return base64.encode(s.encode(encode))
