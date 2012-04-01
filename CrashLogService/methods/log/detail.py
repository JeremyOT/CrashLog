from toto.invocation import *
from bson.objectid import ObjectId

@authenticated
@requires('log_id')
def invoke(handler, parameters):
  log = handler.db.logs.find_one({'_id': ObjectId(parameters['log_id']), 'user_id': handler.session.user_id})
  if not log:
    raise TotoException(1005, 'Log not found')
  del log['_id']
  del log['user_id']
  log['log_id'] = parameters['log_id']
  return log
