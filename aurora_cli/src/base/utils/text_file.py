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

import subprocess
from pathlib import Path

from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps


def file_remove_line(
        file: Path,
        search: str
):
    if file.is_file():
        with open(file, 'r') as f:
            lines = f.readlines()
        with open(file, 'w') as f:
            for line in lines:
                if search not in line:
                    f.write(line)


def file_exist_in_line(
        file: Path,
        search: str
) -> bool:
    if file.is_file():
        with open(file, 'r') as f:
            for line in f.readlines():
                if search in line:
                    return True
    return False


@check_dependency(DependencyApps.sudo)
def file_permissions_777(path: Path):
    if path.is_file():
        for arg in [['sudo', 'chmod', '777', str(path)]]:
            subprocess.call(arg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@check_dependency(DependencyApps.sudo)
def file_permissions_644(path: Path):
    if path.is_file():
        for arg in [
            ['sudo', 'chmod', '644', str(path)],
            ['sudo', 'chown', 'root:root', str(path)]
        ]:
            subprocess.call(arg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
