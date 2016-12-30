import json
import base64

import docker

from sumatra import helpers


engine = docker.from_env()


def run(name, path=None, data=None, args=None, namespace='sumatraio', platform='python', version='2.7', as_json=True, auto_kill=True):
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
  ouput = engine.containers.run(image, params, name=name)
  if auto_kill is True:
    cleanup(name)
  return ouput


def cleanup(container_name, force=True):
  try:
    container = engine.containers.get(container_name)
  except docker.errors.NotFound:
    pass
  except docker.errors.APIError:
    pass
  container.remove(v=True, force=force)
