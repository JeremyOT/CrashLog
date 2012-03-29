from toto.invocation import *

valid_keys = {
  "CallStackSymbols",
  "Signal",
  "Thread",
  "CurrentQueue",
  "ExceptionDescription",
  "Version",
  "ShortVersion",
  "Platform",
  "PlatformVersion",
  "Model",
  "AdditionalInformation",
  "CrashDate"
}

@requires('account_id', 'logs')
def invoke(handler, parameters):
  account = handler.db.accounts.find_one({'account_id': parameters['account_id']}, {'user_id': 1})
  if not account:
    raise TotoException(1000, 'Invalid account ID')
  user_id = account['user_id']
  logs = parameters['logs']
  for log in logs:
    for k in log:
      if k not in valid_keys:
        raise TotoException(1001, 'Invalid log data')
    log['crash_log_user_id'] = user_id
  handler.db.logs.insert(logs)
  return {'logs_added': len(logs)}
