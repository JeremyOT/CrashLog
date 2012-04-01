from toto.invocation import *

@authenticated
def invoke(handler, parameters):
  return {'account_id': handler.session.get_account()['account_id']}
