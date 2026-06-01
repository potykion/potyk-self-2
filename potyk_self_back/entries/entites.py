from sqlalchemy.orm import mapped_column, Mapped

from potyk_self_back.core.db import db


class DiaryEntry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=True)
