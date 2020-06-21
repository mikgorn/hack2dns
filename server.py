from typing import *
from pathlib import Path
from datetime import datetime
from logging import getLogger, INFO, basicConfig

from flask import Flask, render_template, request, redirect, make_response

import tld
import utils
import config
from models import User, Roles
from database import Database
from mail_sender import SecureMailSender


DAY = 24 * 60 * 60
MIN_PASSWORD_LEN = 4

DEFAULT_USERNAME = "Уважаемый Пользователь"


app = Flask(__name__)


_logger = getLogger(__file__)
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

tld.initialize_tld(tld_file_path=config.TLD_FILE_PATH)


class Server:
    def __init__(self, database: Database, mail_sender: SecureMailSender):
        self._database = database
        self._mail_sender = mail_sender

    @staticmethod
    def validate_registration_data(data: Dict[str, Any]) -> Optional[str]:
        for c in "0123456789/@#$%^&*()_=-+}{,.":
            if c in (
                "".join(
                    [
                        data["first_name"],
                        data["second_name"],
                        data["patronymic"],
                    ]
                )
            ):
                return "Некорректный символ в имени"
        if not data["second_name"]:
            return "Фамилия отсутствует"
        if not data["first_name"]:
            return "Имя отсутствует"
        email = data["email"]
        if not utils.is_correct_email(email):
            return "Некорректный email-адрес"
        if data["email"] != data["confirm_email"]:
            return "Адреса электронной почты не совпадают"
        email = utils.convert_email_from_punycode_to_utf(email)
        if not utils.is_domain_exist(utils.get_domain_from_email(email)):
            return "Домен '%s' не существует" % utils.get_domain_from_email(
                email
            )
        if not tld.is_correct_email_tld(email):
            return "Некорректный домен верхнего уровня"
        if _database.get_user_by_email(email) is not None:
            return "Такая почта уже зарегестрирована"
        if len(data["password"]) < MIN_PASSWORD_LEN:
            return (
                "Слишком короткий пароль. Минимальная длина: %s"
                % MIN_PASSWORD_LEN
            )
        if data["password"] != data["confirmpassword"]:
            return "Пароли не совпадают"
        return None

    @staticmethod
    @app.route("/", methods=["POST", "GET"])
    def index():
        return render_template("index.html")

    @staticmethod
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            if not utils.is_correct_email(request.form["email"].lower()):
                return render_template(
                    "index.html", error="Введите корректный email"
                )
            email = utils.convert_email_from_punycode_to_utf(
                request.form["email"].lower()
            )
            password = request.form["pwd"]

            user = _database.get_user_by_email(email)
            if user is None:
                return render_template(
                    "index.html", error="Пользователь не найден"
                )
            if (email != "") and (
                utils.get_password_hash(password) == user.password
            ):
                resp = make_response(
                    render_template("profile.html", user=user)
                )
                resp.set_cookie("email", user.email)
                resp.set_cookie("role", str(int(user.role)))
                return resp
            return render_template("index.html", error="Неверный пароль")
        return render_template("index.html")

    # Регистрация
    @staticmethod
    @app.route("/registration", methods=["POST", "GET"])
    def register():
        error = None
        if request.method == "POST":

            bad_check_results = Server.validate_registration_data(request.form)
            if bad_check_results:
                _logger.info(bad_check_results)
                return render_template(
                    "registration.html", error=bad_check_results
                )
            user = User.create_from_registration_form(request.form)
            _database.set_user(user)
            # Рендер следующей страницы
            resp = make_response(render_template("profile.html", user=user))
            resp.set_cookie("email", user.email)
            resp.set_cookie("role", str(int(user.role)))
            return resp
        return render_template("registration.html")

    @staticmethod
    @app.route("/profile")
    def profile():
        email = request.cookies.get("email")
        if email is not None:
            user = _database.get_user_by_email(email)
            return render_template("profile.html", user=user)
        return redirect("/")

    @staticmethod
    @app.route("/admin")
    def admin():
        role = request.cookies.get("role")
        if role is not None:
            if int(role) == Roles.ADMIN:
                users = _database.get_all_users()
                return render_template("admin.html", users=users)
        return render_template("index.html", error="Недостаточно прав")

    @staticmethod
    @app.route("/spam", methods=["POST", "GET"])
    def spam():
        message = request.form.get("message")
        if request.form.get("send_one") is not None:
            email = request.form.get("email")
            if not utils.is_correct_email(email):
                return render_template(
                    "admin.html",
                    error="Неверный формат email",
                    users=_database.get_all_users(),
                )
            if not utils.is_domain_exist(utils.get_domain_from_email(email)):
                return render_template(
                    "admin.html",
                    error="Домен '%s' не существует"
                    % utils.get_domain_from_email(email),
                    users=_database.get_all_users(),
                )
            email = utils.convert_email_from_punycode_to_utf(email)
            user = _database.get_user_by_email(email)
            if user is None:
                mails = {
                    email: message.replace("_username_", DEFAULT_USERNAME)
                }
            else:
                mails = {email: message.replace("_username_", user.first_name)}
            answer = _mail_sender.send_messages(mails)
            _logger.info(answer)
            return render_template(
                "admin.html", answer=answer, users=_database.get_all_users()
            )

        if request.form.get("spam") is not None:
            users = _database.get_all_users()
            mails = {}
            for user in users:
                if (request.form["address"] == "Все города") or (
                    request.form["address"] == user.address
                ):
                    mails[user.email] = message.replace(
                        "_username_", user.first_name
                    )
            answer = _mail_sender.send_messages(mails)
            _logger.info(answer)
            return render_template("admin.html", answer=answer, users=users)

    @staticmethod
    @app.route("/send_one", methods=["POST", "GET"])
    def send_one():
        mails = {request.form["email"]: "You are the chosen one"}
        answer = _mail_sender.send_messages(mails)
        _logger.info(answer)
        return render_template(
            "admin.html", answer=answer, users=_database.get_all_users()
        )


if __name__ == "__main__":
    basicConfig(level=INFO)
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT)
