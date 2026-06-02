from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    id = StringField("ID")
    title = StringField(
        "Title",
        render_kw={
            "placeholder": "Название",
            "class": "text-input",
        },
    )
    text = TextAreaField(
        "New Entry",
        validators=[DataRequired()],
        render_kw={
            "required": True,
            "placeholder": "Новая запись",
            "rows": 3,
        },
    )
    tags = StringField(
        "Tags",
        render_kw={
            "placeholder": "Теги",
            "class": "tags-input",
        },
    )
    datetime_msk = DateTimeLocalField()
