import os
from datetime import datetime


def gen_file_name(before: str, extension: str) -> str:
    return '{before}{time}.{extension}'.format(
        before=before,
        time=datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        extension=extension
    )


def convert_relative_path(path: str) -> str:
    if path.startswith('~/'):
        path = os.path.expanduser(path)
    if path.startswith('./'):
        path = '{}{}'.format(os.getcwd(), path[1:])
    if path.startswith('../'):
        path = '{}/{}'.format(os.getcwd(), path)
    return path
