from toto.invocation import *
from time import mktime

@authenticated
@requires('app_id')
def invoke(handler, parameters):
  return [{'log_id': str(l['_id']), 'description': l['exception_description'], 'timestamp': mktime(l['timestamp'].timetuple()), 'device': l['device'], 'os_version': l['os_version'], 'app_version': l['short_version']} for l in handler.db.logs.find({'user_id': handler.session.user_id, 'app_id': parameters['app_id']}, sort=[('timestamp', -1),])]
