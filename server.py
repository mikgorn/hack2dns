from typing import *
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)


_current_path: Path = Path(__file__).parent


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration")
def register():
    return render_template("registration.html")

if __name__ == "__main__":
    app.run()
