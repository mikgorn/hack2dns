from sqlite3 import *

class Database:
    def __init__(self, dbfile):
        self.connection = connect(dbfile)
        self.c = self.connection.cursor()

    def initialize(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS users  (id text, firstname text, secondname text, patronymic text, age datetime, email text, password text )")
        self.connection.commit()