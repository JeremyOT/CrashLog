from toto.invocation import *

@authenticated
@requires('app_id')
def invoke(handler, parameters):
  handler.db.apps.remove({'user_id': handler.session.user_id, 'app_id': parameters['app_id']})
  handler.db.logs.remove({'user_id': handler.session.user_id, 'app_id': parameters['app_id']})
  return {'app_id': parameters['app_id']}
