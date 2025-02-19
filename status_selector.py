import collections
import subprocess
from typing import Optional

Status = collections.namedtuple("Status", ["emoji", "text", "until"])


class StatusSelector:
    def __init__(self, environments):
        self._environments = environments

    def select_status(self) -> Optional[Status]:
        active_connections = _get_active_connections()
        for environment_name, environment in self._environments.items():
            if environment["network"] in active_connections:
                return Status(
                    environment["emoji"],
                    environment["text"],
                    environment["until"]
                )


def _get_active_connections() -> str:
    result = subprocess.run(
        ["netsh", "wlan", "show", "interface"],
        capture_output=True,
        check=True,
        shell=True
    )
    for line in result.stdout.splitlines():
        if b"SSID" in line:
            output = line.split(b":")[1].strip().decode()
            return output
