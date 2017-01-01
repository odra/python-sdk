import json
import base64
import uuid

import docker

from sumatra import helpers


_engine = None


def bootstrap(url='unix://var/run/docker.sock'):
  """
  Bootstraps the docker remote api server to be used.

  param: url(str) - URL to be used when making requests to the docker remote api.
  """
  global _engine
  _engine = docker.DockerClient(base_url=url)


def run(name=None, path=None, data=None, args=None, namespace='sumatraio',
  platform='python', version='2.7', as_json=True, auto_kill=True):
  """
  Runs a container to make the remote function call and returns its response.

  param: name(str) - The container name to be used (uses function name if it is not provided)
  param: path(str) - file path to container the code object when running the container
  param: data(Function) - Function object (base64 json) to be sent to the container to run its code object function 
  param: args(list or dict) - A list or dict to be used when calling the remote function
  param: namespace(str) - Namespace to be used when in the image name (default is sumatraio)
  param: platform(str) - Platform to run the remote function call (default is python)
  param: version(str) - Version (tag) for the platform to be used (default is 2.7)
  param: as_json(bool) - Indicates if the returned value should be in json format or plain text.
  param: auto_kill(bool) - Flag to indicate if the container should be auto destroyed.

  Returns:
    The container output (string or dict)  
  """
  image = '%s/%s:%s' % (namespace, platform, version)
  if args is None:
    args = {}
  params = [
    '--params', base64.b64encode(json.dumps(args).encode('utf8')).decode('utf8')
  ]
  if data is not None:
    params.append('--data')
    params.append('%s' % base64.b64encode(helpers.code_to_json(data).encode('utf8')).decode('utf8'))
    params.append('--encode')
  if as_json is True:
    params.append('--json')
  full_fn_name = helpers.get_fn_name(data).replace('.', '-')
  full_fn_name = '%s-%s' % (full_fn_name, uuid.uuid5(uuid.uuid4(), full_fn_name))
  ouput = _engine.containers.run(image, params, name=full_fn_name)
  if auto_kill is True:
    cleanup(full_fn_name)
  return ouput


def cleanup(container_name, force=True):
  """
  Removes the container and its related volumes.

  param: container_name(str) - container name or unique identifier.
  param: force(bool) - Flag to force container removal including its volumes (default is True).
  """
  try:
    container = _engine.containers.get(container_name)
  except docker.errors.NotFound:
    pass
  except docker.errors.APIError:
    pass
  container.remove(v=True, force=force)
