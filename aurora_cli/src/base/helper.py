import os
import re
from datetime import datetime
from pathlib import Path


def gen_file_name(before: str, extension: str) -> str:
    return '{before}{time}.{extension}'.format(
        before=before,
        time=datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        extension=extension
    )


def convert_relative_path(path: str | None) -> Path | None:
    if path is None:
        return None
    if path.startswith('~/'):
        path = os.path.expanduser(path)
    if path.startswith('./'):
        path = '{}{}'.format(os.getcwd(), path[1:])
    if path.startswith('../'):
        path = '{}/{}'.format(os.getcwd(), path)
    return Path(path)


def clear_str_line(line: str) -> str:
    line = line.strip()
    line = str(re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]').sub('', line))
    # I don't know how to humanely clear a line from this ***
    line = str(re.sub(r'\u0000|\u001b8|\u001b7', '', line))
    line = str(re.sub(r'\s+', ' ', line))
    return line
