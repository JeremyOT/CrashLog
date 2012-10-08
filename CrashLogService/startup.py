
def on_start(db_connection, **kwargs):

  account_indexes = db_connection.db.accounts.index_information()
  if 'account_id' not in account_indexes:
    db_connection.db.accounts.ensure_index([('account_id', 1),], name='account_id')

  app_indexes = db_connection.db.apps.index_information()
  if 'user_id_app_id' not in app_indexes:
    db_connection.db.apps.ensure_index([('user_id', 1), ('app_id', 1)], name='user_id_app_id')

  log_indexes = db_connection.db.logs.index_information()
  if 'user_id_app_id_timestamp' not in log_indexes:
    db_connection.db.logs.ensure_index([('user_id', 1), ('app_id', 1), ('timestamp', -1)], name='user_id_app_id_timestamp')
  if '_id_user_id' not in log_indexes:
    db_connection.db.logs.ensure_index([('_id', 1), ('user_id', 1)], name='_id_user_id')
