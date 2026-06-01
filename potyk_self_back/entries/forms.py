from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    id = StringField("ID")
    title = StringField(
        "Title",
        render_kw={"placeholder": "Title"},
    )
    text = TextAreaField(
        "New Entry",
        validators=[DataRequired()],
        render_kw={"required": True, "rows": 5, "placeholder": "New Entry"},
    )
