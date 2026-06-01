import os

from flask import Flask

from potyk_self_back.core.db import db
from potyk_self_back.entries.pres import entries_blueprint
from potyk_self_back.login.pres import setup_login


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["FLASK_SECRET"]

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///potyk-self-2.db"
    db.init_app(app)

    setup_login(app)

    app.register_blueprint(entries_blueprint)

    return app
