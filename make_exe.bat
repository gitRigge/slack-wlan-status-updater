ECHO Build Executable
pyinstaller ^
        --onefile ^
        --noconsole ^
        --distpath .\bin ^
        --workpath .\build ^
        --paths %cd%\ ^
        --clean ^
        --log-level INFO ^
        --hidden-import event_selector ^
        --hidden-import status_selector ^
        --hidden-import status_setter ^
        --hidden-import pathlib ^
        --hidden-import tomllib ^
        --hidden-import typing ^
        --hidden-import collections ^
        --hidden-import subprocess ^
        --hidden-import datetime ^
        --hidden-import date ^
        --hidden-import timedelta ^
        --hidden-import locale ^
        --hidden-import caldav ^
        --hidden-import caldav.davclient ^
        --name SlackStatusChanger ^
        --add-data %cd%\*.py;\ ^
        --clean ^
    __main__.py