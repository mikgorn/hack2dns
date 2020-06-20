from typing import *
from pathlib import Path

from flask import Flask, render_template, request, redirect, make_response
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

            user = User.create_from_registration_form(request.form)
            db.set_user(user)
            # Рендер следующей страницы
            resp = make_response(render_template("profile.html",user=user))
            resp.set_cookie('email', request.form["email"])
            return redirect("/profile")
        return render_template("registration.html")

    @staticmethod
    @app.route("/profile")
    def profile():
        email = request.cookies.get("email")
        if(email!=""):
            user=db.get_user_by_email(email)
            return render_template("profile.html",user=user)

if __name__ == "__main__":
    db = Database("hack2.db")
    db.initialize()
    app.run()
