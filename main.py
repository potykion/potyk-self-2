import os

from flask import Flask

from potyk_self_back.core.db import db
from potyk_self_back.entries.pres import entries_blueprint
from potyk_self_back.login.pres import setup_login


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["FLASK_SECRET"]

    db_name = os.environ.get("DB_FILE_NAME", "potyk-self-2.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_name
    db.init_app(app)

    setup_login(app)

    app.register_blueprint(entries_blueprint)

    return app
