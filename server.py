from typing import *
from pathlib import Path

from flask import Flask, render_template, request
from database import Database
from models import User
from datetime import datetime

app = Flask(__name__)


_current_path: Path = Path(__file__).parent


class Server:
    @staticmethod
    @app.route("/")
    def index():
        return render_template("index.html")

    # Регистрация
    @staticmethod
    @app.route("/registration", methods=["POST", "GET"])
    def register():
        error = None
        if request.method == "POST":

            # Данные из формы регистрации
            print(request.form)
            print(User.create_from_registration_form(request.form))
            # Рендер следующей страницы
            return render_template("registration.html")
        return render_template("registration.html")


if __name__ == "__main__":
    db = Database("hack2.db")
    db.initialize()
    app.run()
