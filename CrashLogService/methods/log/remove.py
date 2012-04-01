from toto.invocation import *
from bson.objectid import ObjectId

@authenticated
@requires('log_id')
def invoke(handler, parameters):
  handler.db.logs.remove({'_id': ObjectId(parameters['log_id']), 'user_id': handler.session.user_id})
  return {'log_id': parameters['log_id']}
