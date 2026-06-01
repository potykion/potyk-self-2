from datetime import datetime

import flask
import pytz
from flask import Blueprint
from flask import request
from flask_login import login_required

from potyk_self_back.core.db import db
from potyk_self_back.core.dt_utils import weekday_to_ru
from potyk_self_back.entries.entites import DiaryEntry
from potyk_self_back.entries.forms import EntryForm

entries_blueprint = Blueprint("entries", __name__)


@entries_blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():

    msk_tz = pytz.timezone("Europe/Moscow")
    msk_now = datetime.now(msk_tz)

    cur_date = msk_now.date()
    cur_date_weekday = weekday_to_ru(cur_date.weekday())

    entries = db.session.execute(db.select(DiaryEntry)).scalars()
    entry_forms = [EntryForm(obj=entry) for entry in entries]

    form = EntryForm()

    if request.method == "POST" and form.validate_on_submit():
        form_data = form.data
        form_data.pop("csrf_token")
        entry = DiaryEntry(**form_data)
        db.session.add(entry)
        db.session.commit()
        return flask.redirect("/")

    return flask.render_template(
        "index.html",
        cur_date=cur_date,
        cur_date_weekday=cur_date_weekday,
        form=form,
        entries=entries,
        entry_forms=entry_forms,
    )


@entries_blueprint.route("/edit-entry/<int:id>", methods=["POST"])
@login_required
def edit_entry(id):
    entry = db.get_or_404(DiaryEntry, id)
    form = EntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.commit()
        return flask.redirect("/")
