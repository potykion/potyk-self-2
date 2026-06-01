from datetime import datetime

import pytz


def get_msk_now() -> datetime:
    msk_tz = pytz.timezone("Europe/Moscow")
    msk_now = datetime.now(msk_tz)
    return msk_now


def weekday_to_ru(weekday):
    return {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье",
    }[weekday]
