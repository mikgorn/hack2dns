from typing import *
from pathlib import Path

from flask import Flask, render_template
from sqlite3 import *
from database import *

app = Flask(__name__)


_current_path: Path = Path(__file__).parent



class Server:

    @staticmethod
    @app.route("/")
    def index():
        return render_template("index.html")

    @staticmethod
    @app.route("/registration")
    def register():
        return render_template("registration.html")

    @staticmethod
    @app.route("/new_user",methods=['POST','GET'])
    def new_user():
        error = None
        if request.method=='POST' :
                return 0

if __name__ == "__main__":
    db = Database("hack2.db")
    db.initialize()
    app.run()
