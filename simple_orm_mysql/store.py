#coding:utf-8
import MySQLdb

class SqlStore(object):
    """
    Wrap mysql connection.
    """

    TIMEOUT_INTERVAL = 6 * 3600

    def __init__(self, **kwargs):
        self.autocommit = True
        kwargs['charset'] = 'utf8'
        self._con_str = kwargs
        self._conn = None
        self.timeout = None

    def get_cursor(self, dict_format=False):
        if self.is_expire():
            self.close()
            self._connect()
        if dict_format:
            cursor = self._conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        else:
            cursor = self._conn.cursor()
        return cursor

    def _connect(self):
        self._conn = MySQLdb.connect(**self._con_str)
        self.timeout = time.time() + self.TIMEOUT_INTERVAL
        return self._conn

    def is_expire(self):
        return self.timeout is None or self.timeout < time.time()

    def close(self):
        self.cursor.close()
        if self._conn:
            self._conn.close()

    def execute_raw_sql(self,sql, params=None):
        cursor = self.get_cursor()
        return cursor.execute(sql, params) if params else cursor.execute(sql)

if __name__ == '__main__':
    db_config = {
        'host':"127.0.0.1",
        'password':"xiaorui.cc",
        'port':"3306",
        'database':'xiaorui.cc',
    }
    sqlstore = SqlStore(**db_config)
    cursor = sqlstore.get_cursor()
