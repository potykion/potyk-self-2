import flask
from flask import redirect
from flask_login import LoginManager, login_user

from potyk_self_back.login.entries import SecretUser
from potyk_self_back.login.forms import LoginForm


def setup_login(app):
    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(secret):
        return SecretUser(secret)

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect("/login")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.is_submitted():
            if form.validate():
                secret = form.secret.data
                login_user(SecretUser(secret))
                return flask.redirect("/")
            else:
                flask.flash("you fail me", "error")
        return flask.render_template("login.html", form=form)

    login_manager.init_app(app)
