from typing import *
from pathlib import Path

from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime

import config
from models import User
from database import Database
from mail_sender import SecureMailSender


DAY = 24 * 60 * 60


app = Flask(__name__)


_current_path: Path = Path(__file__).parent
_database: Database = Database(Path("hack2.db"))
_database.initialize()
_mail_sender: SecureMailSender = SecureMailSender(
    smtp_host=config.SMTP_HOST,
    smtp_port=config.SMTP_PORT,
    sender_addr=config.SENDER_MAIL,
    password=config.SENDER_PASSWORD,
)


class Server:
    def __init__(self, database: Database, mail_sender: SecureMailSender):
        self._database = database
        self._mail_sender = mail_sender

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

            user = User.create_from_registration_form(request.form)
            _database.set_user(user)
            # Рендер следующей страницы
            resp = make_response(render_template("profile.html", user=user))
            resp.set_cookie("email", request.form["email"])
            return resp
        return render_template("registration.html")

    @staticmethod
    @app.route("/profile")
    def profile():
        email = request.cookies.get("email")
        if email != "":
            user = _database.get_user_by_email(email)
            return render_template("profile.html", user=user)


if __name__ == "__main__":
    app.run()
