from toto.invocation import *

@authenticated
def invoke(handler, parameters):
  return [{'app_id': i['app_id'], 'name': i['name']} for i in handler.db.apps.find({'user_id': handler.session.user_id})]
