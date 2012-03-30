from toto.invocation import *
from tornado.options import options, define

define('valid_log_keys', metavar='{key set}', type=set, help='A set of keys to use for logs. A post will fail if any of its logs contain keys not in this set')
define('demo_account_valid', metavar='True|False', default=False, help='Whether or not the account_id "DEMO" should be allowed to post logs')

valid_keys = options.valid_log_keys

def retrieve_account(db, account_id):
  account = db.accounts.find_one({'account_id': account_id}, {'user_id': 1})
  if not account:
    raise TotoException(1000, 'Invalid account ID')
  return account['user_id']

if options.demo_account_valid:
  f = retrieve_account
  def retrieve_wrapper(db, account_id):
    if account_id == 'DEMO':
      return 'DEMO'
    return f(db, account_id)
  retrieve_account = retrieve_wrapper

@requires('account_id', 'logs')
def invoke(handler, parameters):
  user_id = retrieve_account(handler.db, parameters['account_id'])
  logs = parameters['logs']
  for log in logs:
    for k in log:
      if k not in valid_keys:
        raise TotoException(1001, 'Invalid log data')
    log['user_id'] = user_id
  handler.db.logs.insert(logs)
  return {'logs_added': len(logs)}
