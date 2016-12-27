from sumatra import errors


def test_base_error():
  err = errors.BaseError(code=1, message='error')
  err.data = {'reason': 'iddqd'}
  assert err.code == 1
  assert err.message == 'error'
  assert err.as_dict()['error']['reason'] == 'iddqd'
  assert type(err.as_json()) is str


def test_credential_error():
  err = errors.CredentialsError()
  assert err.code == -32000
  assert err.message == 'Local credentials not set properly.'
  assert err.as_dict()['error'] is None
  assert type(err.as_json()) is str


