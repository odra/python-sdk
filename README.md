# Sumatra Client

## Installation

```sh
pip install sumatra
```

```sh
python setup.py install
```

### Requirements

See [requirements files](requirements.txt)

## Tests

Uses `pytest` as test runner:

```sh
py.test -s
```

There is also a make file for convenience.

## Simple Usage

For complete api docs and usage see the full documentation at [readthedocs](.).

Create a `.sumatra.yaml` or `sumatra.json` config file in your project root directory

```yaml
sumatra:
  - name: 'myapp'
  - token: '12345'
  server:
    - host: 'fn.sumatra.io'
    - port: 80
    - protocol: 'http'
```

```json
{
  "sumatra": {
    "name": "myapp",
    "token": "12345",
    "server": {
      "protocol": "http",
      "host": "fn.sumatraio",
      "port": 80
    }
  }
}
```


You can manually bootstrap the client at some point

```py
import sumatra

sumatra.bootstrap() #default
sumatra.bootstrap(file='/path_to_file.yaml') #specify yaml path
sumatra.bootstrap('app_name', 'app_token') #manually set "app name" and "token"
```

Add the `sumatra.fn` decorator to remotely process the function and retrieve the result

```py
import sumatra

@sumatra.fn
def hello():
  return 'hello there'

#remote call function
print(hello())
```

## License

Copyright 2016 Leonardo Rossetti <me@lrossetti.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
