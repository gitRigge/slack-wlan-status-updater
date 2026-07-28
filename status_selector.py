import collections
import fnmatch
import socket
import subprocess
from typing import Optional

Status = collections.namedtuple("Status", ["emoji", "text", "until"])


class StatusSelector:
    def __init__(self, environments):
        self._environments = environments

    def select_status(self) -> Optional[Status]:
        active_connections = _get_active_connections()
        if active_connections is not None:
            for environment in self._environments.values():
                if environment["network"] in active_connections:
                    return Status(
                        environment["emoji"],
                        environment["text"],
                        environment["until"]
                    )
        else:
            ip = _get_primary_ip()
            if ip is not None:
                for environment in self._environments.values():
                    if fnmatch.fnmatch(ip, environment["ip"]):
                        return Status(
                            environment["emoji"],
                            environment["text"],
                            environment["until"]
                        )
        return None


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


def _get_primary_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually send data
        s.connect(("192.0.2.1", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
