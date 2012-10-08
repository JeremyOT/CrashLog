import toto.methods.account.login as login
from toto.invocation import *
import uuid
import base64

@requires('user_id', 'password')
def invoke(handler, params):
  handler.db_connection.create_account(params['user_id'], params['password'], {'account_id': '%s%s' % (base64.b64encode(uuid.uuid4().bytes, '-_')[:-2], base64.b64encode(uuid.uuid4().bytes, '-_')[:-2])})
  return login.invoke(handler, params)
