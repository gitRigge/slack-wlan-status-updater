import datetime
import pathlib
import sys
import tomllib

from event_selector import CalendarSelector
from status_selector import StatusSelector
from status_setter import (InterceptingSlackStatusSetterDecorator,
                           MultiStatusSetter, SlackStatusSetter, StatusSetter)


class MainLoop:
    def __init__(
        self,
        event_selector: CalendarSelector,
        status_selector: StatusSelector,
        status_setter: StatusSetter,
    ):
        self._event_selector = event_selector
        self._status_selector = status_selector
        self._status_setter = status_setter

    def run(self) -> None:
        while True:
            if self._event_selector is not None:
                status = self._event_selector.select_status()
            if status.emoji is None:
                status = self._status_selector.select_status()
            if status is None:
                sys.exit(0)
            else:
                emoji, text, until = status
                expiration = datetime.datetime.combine(
                    datetime.date.today(),
                    datetime.datetime.strptime(until, "%H:%M").time()
                )
                try:
                    self._status_setter.set_status(emoji, text, expiration)
                except Exception as e:
                    print(f"Error setting status: {e}")
                sys.exit(0)


def main() -> None:
    config = get_config()
    calendar_selector = None
    if config["caldav"] is not None:
        calendar_selector = build_calendar_selector(config)
    status_selector = build_status_selector(config)
    status_setter = build_status_setter(config)
    main_loop = MainLoop(calendar_selector, status_selector, status_setter)

    main_loop.run()


def get_config() -> dict:
    raw_config_path = "config.toml"
    config_path = pathlib.Path(raw_config_path).expanduser()
    with open(config_path, "rb") as f:
        config = tomllib.load(f)
    return config


def build_calendar_selector(config: dict) -> CalendarSelector:
    return CalendarSelector(config["caldav"])


def build_status_selector(config: dict) -> StatusSelector:
    return StatusSelector(config["environments"])


def build_status_setter(config: dict) -> StatusSetter:
    slack_status_setters = [
        SlackStatusSetter(name, slack["token"])
        for name, slack in config["slack"].items()
    ]
    interceptors = [
        InterceptingSlackStatusSetterDecorator(slack_status_setter)
        for slack_status_setter in slack_status_setters
    ]
    multi = MultiStatusSetter(interceptors)
    return multi


if __name__ == "__main__":
    main()
