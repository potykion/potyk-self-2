from __future__ import annotations

from typing import TYPE_CHECKING

from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, BooleanField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.validators import DataRequired

if TYPE_CHECKING:
    from potyk_self_back.entries.entites import DiaryEntry


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
    pinned = BooleanField(default=False)

    @classmethod
    def from_entry(cls, entry: DiaryEntry) -> EntryForm:
        form = cls(obj=entry)
        # TomSelect expects comma-separated tags; obj=entry gives a list.
        # On POST, request data must not be overwritten by DB values.
        if not form.is_submitted():
            form.tags.data = ",".join(entry.tags or [])
        return form
