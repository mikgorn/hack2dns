from sqlite3 import *


class Database:
    def __init__(self, dbfile):
        self.connection = connect(dbfile)
        self.c = self.connection.cursor()

    def initialize(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS users  (id integer primary key autoincrement, firstname text, secondname text, patronymic text, age datetime, email text, phone text, address text, password text, retiree int, disabled int  )"
        )
        self.connection.commit()
