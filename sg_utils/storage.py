import sqlite3
from .utils import dotdict
import os


def dict_factory(cursor, row):
    d = dotdict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_connect(f, db=None):
    def wrapper(self, *args, **kwargs):
        if self.conn==None:
            self.connect()
            try:
                f_res = f(self, *args, **kwargs)
                return f_res
            except:
                raise
            finally:
                if self.conn!=None:
                    self.close()
        else:
            return f(self, *args, **kwargs)
    return wrapper


class storeBase(object):
    def __init__(self, filepath, writer=True):
        self.db_name = filepath
        self.conn, self.cursor = None, None
        if writer:
            
            try:
                self.connect()
                self.cursor.execute('''PRAGMA journal_mode=WAL;''')
                self.close()
            except:
                pass
            
            # Initial connect process
            self.connect()
            self.create()
            self.close()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn!=None:
            self.conn.commit()
            self.conn.close()
        self.conn, self.cursor = None, None

    def destroy(self):
        self.close()
        os.system('rm {}'.format(self.db_name))

    def create(self, *args, **kwargs):
        raise StoreBaseClassError('Subclass StoreBase and implement create() method')

    @db_connect
    def checkForTables(self, tables):
        for name in tables:
            tableExists = self.cursor.execute("SELECT count(*) as c FROM sqlite_master WHERE type='table' AND name=?;", (name, )).fetchone()
            if not tableExists['c']:
                return False
        return True


class StoreBaseClassError(Exception):
    pass

if __name__ == '__main__':
    s = storeBase('./test.db')
