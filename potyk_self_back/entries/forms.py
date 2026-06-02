from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.fields.datetime import DateTimeLocalField
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
        render_kw={
            "required": True,
            "placeholder": "New Entry",
            "rows": 3,
        },
    )
    tags = StringField(
        "Tags",
        render_kw={"placeholder": "Теги"},
    )
    datetime_msk = DateTimeLocalField()
