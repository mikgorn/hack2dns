from typing import *
from pathlib import Path

from flask import Flask, render_template
from sqlite3 import *

app = Flask(__name__)


_current_path: Path = Path(__file__).parent

class Database:
    def __init__(self, dbfile):
        self.connection = connect(dbfile)
        self.c = self.connection.cursor()

    def initialize(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS users  (id text, firstname text, secondname text, patronymic text, age datetime, email text, password text )")
        self.connection.commit()


class Server:

    @staticmethod
    @app.route("/")
    def index():
        return render_template("index.html")

    @staticmethod
    @app.route("/registration")
    def register():
        return render_template("registration.html")



if __name__ == "__main__":
    db = Database("hack2.db")
    db.initialize()
    app.run()
