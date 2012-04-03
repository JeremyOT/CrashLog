from toto.invocation import *
from bson.objectid import ObjectId
from time import mktime

@authenticated
@requires('log_id')
def invoke(handler, parameters):
  log = handler.db.logs.find_one({'_id': ObjectId(parameters['log_id']), 'user_id': handler.session.user_id})
  if not log:
    raise TotoException(1005, 'Log not found')
  del log['_id']
  del log['user_id']
  log['log_id'] = parameters['log_id']
  log['timestamp'] = mktime(log['timestamp'].timetuple())
  log['backtrace']
  backtrace = [(int(t.split(' ', 1)[0]), t) for t in log['backtrace']]
  backtrace.sort()
  log['backtrace'] = [t[1] for t in backtrace]
  return log
