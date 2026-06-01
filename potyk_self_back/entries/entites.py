from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped

from potyk_self_back.core.db import db
from potyk_self_back.core.dt_utils import get_msk_now


class DiaryEntry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=True)
    datetime_msk: Mapped[datetime] = mapped_column(
        nullable=False,
        default=get_msk_now,
    )
