from typing import *
from pathlib import Path
from datetime import datetime
from logging import getLogger, INFO

from flask import Flask, render_template, request, redirect, make_response

import tld
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
    def validate_registration_data(data: Dict[str, Any]) -> Optional[str]:
        if data["password"] != data["confirmpassword"]:
            return "Пароли не совпадают!"
        if not tld.is_correct_email_tld(data["email"]):
            return "Некоректный домен верхнего уровня!"
        return None

    @staticmethod
    @app.route("/", methods=["POST", "GET"])
    def index():
        return render_template("index.html")

    @staticmethod
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            email = utils.convert_email_from_punycode_to_utf(
                request.form["email"].lower()
            )
            password = request.form["pwd"]

            user = _database.get_user_by_email(email)
            if (email != "") and (
                utils.get_password_hash(password) == user.password
            ):
                resp = make_response(
                    render_template("profile.html", user=user)
                )
                resp.set_cookie("email", user.email)
                return resp
        return render_template("index.html")

    # Регистрация
    @staticmethod
    @app.route("/registration", methods=["POST", "GET"])
    def register():
        error = None
        if request.method == "POST":

            bad_check_results = Server.validate_registration_data(request.form)
            if bad_check_results:
                print(bad_check_results)
                return render_template("registration.html")
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
        answer = _mail_sender.send_messages(mails)
        print(answer)
        return render_template("admin.html", answer=answer)

    @staticmethod
    @app.route("/send_one", methods=["POST", "GET"])
    def send_one():
        mails = {request.form["email"]: "You are the chosen one"}
        answer = _mail_sender.send_messages(mails)
        print(answer)
        return render_template("admin.html", answer=answer)


if __name__ == "__main__":
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT)
