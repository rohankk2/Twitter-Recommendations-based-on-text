import sqlite3
from sqlite3 import Error

class dbFactory:
    def __init__(self):
        self.db_file = r"db/pythonsqlite.db"
        self.conn = None
    def set_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
    def get_connection(self):
        return self.conn