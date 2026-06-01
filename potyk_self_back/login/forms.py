import os

from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, AnyOf


class LoginForm(FlaskForm):
    secret = StringField(
        validators=[
            DataRequired(),
            AnyOf([os.environ["FLASK_SECRET"]]),
        ],
        render_kw={"required": True, "placeholder": "Enter secret"},
    )
