from toto.invocation import *

@authenticated
@requires('app_id', 'name')
def invoke(handler, parameters):
  if handler.db.apps.find_one({'app_id': parameters['app_id'], 'user_id': handler.session.user_id}):
    raise TotoException(1002, 'App ID already exists')
  handler.db.apps.insert({'user_id': handler.session.user_id, 'app_id': parameters['app_id'], 'name': parameters['name']})
  return {'app_id': parameters['app_id'], 'name': parameters['name']}
