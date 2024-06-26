from functools import wraps
from flask import current_app, abort
from mysql.connector import Error

def with_cnx(need_commit = None):
  def decorator(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
      cnx = current_app.db_cnx()
      cursor = cnx.cursor()
      try:
        result = func(cursor, *args, **kwargs)
        if need_commit:
          cnx.commit()
      except Error as e:
        cnx.rollback()
        abort(500, description=f'Exception raise in utils/with_cnx: {e}')
      finally:
        cursor.close()
        cnx.close()
      return result
    return decorated_func
  return decorator