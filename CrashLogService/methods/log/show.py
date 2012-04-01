from toto.invocation import *
from time import mktime

@authenticated
@requires('app_id')
def invoke(handler, parameters):
  return [{'log_id': str(l['_id']), 'description': l['exception_description'], 'friendly_time': str(l['timestamp']), 'timestamp': mktime(l['timestamp'].timetuple()), 'model': l['model']} for l in handler.db.logs.find({'user_id': handler.session.user_id, 'app_id': parameters['app_id']}, sort=[('timestamp', -1),])]
