from sumatra import errors
from sumatra import client
from sumatra import fn


def bootstrap(*args, **kwargs):
  """
  Wrapper function that calls sumatra.client.
  """
  return client.bootstrap(*args, **kwargs)


def function(*args, **kwargs):
  """
  Wrapper function that calls sumatra.fn.fn.
  """
  return fn.fn(*args, **kwargs)

