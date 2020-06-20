from typing import *
from pathlib import Path
from datetime import datetime
from logging import getLogger, INFO

from flask import Flask, render_template, request, redirect, make_response

import config
from models import User
from database import Database
from mail_sender import SecureMailSender
import utils


DAY = 24 * 60 * 60


app = Flask(__name__)


_logger = getLogger(__file__)
_logger.setLevel(INFO)
_current_path: Path = Path(__file__).parent
_database: Database = Database(Path("hack2.db"))
_database.initialize()
_mail_sender: SecureMailSender = SecureMailSender(
    smtp_host=config.SMTP_HOST,
    smtp_port=config.SMTP_PORT,
    sender_addr=config.SENDER_MAIL,
    password=config.SENDER_PASSWORD,
)
_mail_sender.start()


class Server:
    def __init__(self, database: Database, mail_sender: SecureMailSender):
        self._database = database
        self._mail_sender = mail_sender

    @staticmethod
    @app.route("/", methods=["POST", "GET"])
    def index():
        return render_template("index.html")

    @staticmethod
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            print(request.form)
            email = utils.convert_email_from_punycode_to_utf(
                request.form["email"]
            )
            password = request.form["pwd"]

            user = _database.get_user_by_email(email)
            print(user)
            print(utils.get_password_hash(password))
            if (email != "") and (
                utils.get_password_hash(password) == user.password
            ):
                resp = make_response(
                    render_template("profile.html", user=user)
                )
                resp.set_cookie("email", request.form["email"])
                return resp
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
            resp.set_cookie("email", user.email)
            return resp
        return render_template("registration.html")

    @staticmethod
    @app.route("/profile")
    def profile():
        email = request.cookies.get("email")
        if email != "":
            user = _database.get_user_by_email(email)
            return render_template("profile.html", user=user)
        return redirect("/")

    @staticmethod
    @app.route("/admin")
    def admin():
        return render_template("admin.html")

    @staticmethod
    @app.route("/spam")
    def spam():
        users = _database.get_all_users()
        mails = {u.email: "SPAAAAM!!!" for u in users}
        _logger.info(str(_mail_sender.send_messages(mails)))
        return render_template("admin.html")


if __name__ == "__main__":
    app.run()
