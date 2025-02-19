ECHO Build Executable
pyinstaller ^
        --onefile ^
        --noconsole ^
        --distpath .\bin ^
        --workpath .\build ^
        --paths %cd%\ ^
        --clean ^
        --log-level INFO ^
        --hidden-import status_selector ^
        --hidden-import status_setter ^
        --hidden-import pathlib ^
        --hidden-import tomllib ^
        --hidden-import typing ^
        --hidden-import collections ^
        --hidden-import subprocess ^
        --hidden-import datetime ^
        --name slack-wlan-status-updater ^
        --add-data %cd%\*.py;\ ^
        --clean ^
    __main__.py