"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from datetime import datetime
from os.path import basename
from pathlib import Path
from typing import Any


def path_gen_file_name(
        before: str,
        extension: str
) -> str:
    return '{before}{time}.{extension}'.format(
        before=before,
        time=datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
        extension=extension
    )


def path_convert_relative(path: Any) -> Any:
    if path is None:
        return None
    if not isinstance(path, str):
        return None
    if path.startswith('~/'):
        path = os.path.expanduser(path)
    if path.startswith('./'):
        path = '{}{}'.format(os.getcwd(), path[1:])
    if path.startswith('../'):
        path = '{}/{}'.format(os.getcwd(), path)
    return Path(path)


def path_get_download_path(url: str) -> Path:
    return path_get_download_folder() / basename(url)


def path_get_download_folder() -> Path:
    default = Path.home() / "Downloads"
    check_folder = [
        Path.home() / "Загрузки",
        default
    ]
    for item in check_folder:
        if item.is_dir():
            return item
    default.mkdir(parents=True, exist_ok=True)
    return default
