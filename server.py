from typing import *
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)


_current_path: Path = Path(__file__).parent


class Server:

    @staticmethod
    @app.route("/")
    def index():
        return render_template("index.html")

    @staticmethod
    @app.route("/register")
    def register():
        return render_template("register.html")


if __name__ == "__main__":
    app.run()
