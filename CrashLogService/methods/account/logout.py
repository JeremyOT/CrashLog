from toto.invocation import *

@authenticated
def invoke(handler, params):
  handler.db.sessions.remove({'session_id': handler.session.session_id})
  return {'authenticated': False}
