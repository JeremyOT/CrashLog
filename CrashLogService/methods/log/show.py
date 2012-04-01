from toto.invocation import *

@authenticated
@requires('app_id')
def invoke(handler, parameters):
  return [{'log_id': str(l['_id']), 'description': l['exception_description'], 'timestamp': l['timestamp'], 'model': l['model']} for l in handler.db.logs.find({'user_id': handler.session.user_id, 'app_id': parameters['app_id']}, sort=[('timestamp', -1),])]
