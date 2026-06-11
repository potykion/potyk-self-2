import random

import flask
from flask import Blueprint
from flask import request
from flask_login import login_required
from sqlalchemy import func

from potyk_self_back.core.db import db
from potyk_self_back.core.dt_utils import weekday_to_ru, get_msk_now
from potyk_self_back.entries.entites import DiaryEntry
from potyk_self_back.entries.forms import EntryForm

entries_blueprint = Blueprint("entries", __name__)


def _parse_tags(raw_tags: str | None) -> list[str]:
    if not raw_tags:
        return []

    tags = [tag.strip() for tag in raw_tags.split(",")]
    # Keep insertion order and drop empty/duplicate tags.
    return list(dict.fromkeys(tag for tag in tags if tag))


@entries_blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():
    msk_now = get_msk_now()
    cur_date = msk_now.date()
    cur_date_weekday = weekday_to_ru(cur_date.weekday())

    selected_tag = flask.request.values.get("tag")

    q = db.select(DiaryEntry).order_by(DiaryEntry.datetime_msk.desc())
    if selected_tag:
        tag_elem = func.json_each(DiaryEntry.tags).table_valued(
            "value",
            joins_implicitly=True,
        )
        q = q.where(tag_elem.c.value == selected_tag)
    entries = db.session.execute(q).scalars().all()
    active_entries = [entry for entry in entries if not entry.archived]

    pinned_entries = [entry for entry in active_entries if entry.pinned]
    regular_entries = [entry for entry in active_entries if not entry.pinned]

    pinned_entry_forms = [EntryForm.from_entry(entry) for entry in pinned_entries]
    regular_entry_forms = [EntryForm.from_entry(entry) for entry in regular_entries]

    archived_q = db.select(DiaryEntry).where(DiaryEntry.archived.is_(True)).order_by(
        DiaryEntry.datetime_msk.desc()
    )
    archived_entries = db.session.execute(archived_q).scalars().all()
    archived_entry_forms = [EntryForm.from_entry(entry) for entry in archived_entries]

    all_tags = sorted(
        {
            tag
            for tags in db.session.execute(db.select(DiaryEntry.tags)).scalars()
            for tag in (tags or [])
            if tag
        }
    )

    if active_entries:
        random_entry: DiaryEntry = random.choice(active_entries)
        random_entry_form: EntryForm | None = EntryForm.from_entry(random_entry)
    else:
        random_entry_form = None

    form = EntryForm()
    if request.method == "POST" and form.validate_on_submit():
        form_data = form.data
        form_data.pop("csrf_token")
        form_data["tags"] = _parse_tags(form_data.get("tags"))
        entry = DiaryEntry(**form_data)
        db.session.add(entry)
        db.session.commit()
        return flask.redirect("/")

    return flask.render_template(
        "index.html",
        cur_date=cur_date,
        cur_date_weekday=cur_date_weekday,
        form=form,
        pinned_entry_forms=pinned_entry_forms,
        regular_entry_forms=regular_entry_forms,
        archived_entry_forms=archived_entry_forms,
        all_tags=all_tags,
        random_entry_form=random_entry_form,
        selected_tag=selected_tag,
    )


@entries_blueprint.route("/edit-entry/<int:id>", methods=["POST"])
@login_required
def edit_entry(id):
    entry = db.get_or_404(DiaryEntry, id)

    if request.form.get("action") == "delete":
        db.session.delete(entry)
        db.session.commit()
        if request.headers.get("HX-Request"):
            return "", 200
        return flask.redirect("/")

    if request.form.get("action") == "toggle-pin":
        entry.pinned = not entry.pinned
        db.session.commit()
        return flask.redirect("/")

    if request.form.get("action") == "toggle-archive":
        entry.archived = not entry.archived
        if entry.archived:
            entry.pinned = False
        db.session.commit()
        if request.headers.get("HX-Request"):
            return "", 200
        return flask.redirect("/")

    form = EntryForm.from_entry(entry)
    if form.validate_on_submit():
        entry.title = form.title.data
        entry.text = form.text.data
        entry.datetime_msk = form.datetime_msk.data
        entry.tags = _parse_tags(form.tags.data)
        db.session.commit()
        form = EntryForm.from_entry(entry)
        form.tags.data = ",".join(entry.tags or [])
    pin_title = "Открепить" if entry.pinned else "Закрепить"
    return flask.render_template(
        "_partials/entry_form.html",
        entry_form=form,
        pin_title=pin_title,
    )
