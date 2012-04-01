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

def retrieve_app(db, user_id, app_id):
  app = db.apps.find_one({'user_id': user_id, 'app_id': app_id})
  if not app:
    raise TotoException(1003, 'Invalid app ID')
  return app

if options.demo_account_valid:
  retrieve_account_base = retrieve_account
  def retrieve_account_wrapper(db, account_id):
    if account_id == 'DEMO':
      return 'DEMO'
    return retrieve_account_base(db, account_id)
  retrieve_account = retrieve_account_wrapper
  retrieve_app_base = retrieve_app
  def retrieve_app_wrapper(db, user_id, app_id):
    if user_id == 'DEMO':
      return {'user_id': 'DEMO', 'app_id': 'DEMO', 'name': 'DEMO'}
    return retrieve_app_base(db, user_id, app_id)
  retrieve_app = retrieve_app_wrapper

@requires('account_id', 'logs', 'app_id')
def invoke(handler, parameters):
  user_id = retrieve_account(handler.db, parameters['account_id'])
  app = retrieve_app(handler.db, user_id, parameters['app_id'])
  logs = parameters['logs']
  for log in logs:
    for k in log:
      if k not in valid_keys:
        raise TotoException(1001, 'Invalid log data')
    log['user_id'] = user_id
    log['app_id'] = app['app_id']
  handler.db.logs.insert(logs)
  return {'logs_added': len(logs)}
