import collections
import locale
from datetime import date, timedelta
from typing import Optional

import caldav

Status = collections.namedtuple("Status", ["emoji", "text", "until"])


class CalendarSelector:
    def __init__(self, settings):
        self._settings = settings

    def select_status(self) -> Optional[Status]:
        try:
            with caldav.get_davclient(
                    username=self._settings["username"],
                    password=self._settings["password"],
                    url=self._settings["url"]) as client:
                _principal = client.principal()
                _calendars = _principal.get_calendars()
                _cal_name = self._settings["calendar_name"]
                _cal = _get_calendar(_calendars, _cal_name)
                self._events = _get_todays_events(_cal)
        except Exception:
            self._events = []
        emoji = None
        text = None
        if _is_weekend():
            emoji = "couch_and_lamp"
            text = "Weekend"
            if locale.getlocale()[0] == "de_DE":
                text = "Wochenende"
        if _is_vacation(self._events):
            emoji = "palm_tree"
            text = "Vacation"
            if locale.getlocale()[0] == "de_DE":
                text = "Urlaub"
        return Status(
            emoji,
            text,
            "23:59"
        )


def _get_calendar(
        calendars: list[caldav.Calendar],
        calendar_name: str) -> caldav.Calendar:
    for cal in calendars:
        if cal.name == calendar_name:
            return cal


def _get_todays_events(calendar: caldav.Calendar) -> dict:
    return calendar.search(
        event=True,
        start=date.today(),
        end=date.today() + timedelta(days=1),
        expand=True)


def _is_weekend() -> bool:
    return date.today().weekday() >= 5


def _is_vacation(events: dict) -> bool:
    for event in events:
        if event.data.find("acation") != -1:
            return True
        if event.data.find("rlaub") != -1:
            return True
    return False
