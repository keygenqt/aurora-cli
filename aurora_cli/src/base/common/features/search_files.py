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

from pathlib import Path
from typing import Any

from aurora_cli.src.base.utils.verbose import verbose_command_start, verbose_add_map


def search_files(
        workdir: Path,
        pattern: str
) -> [Path]:
    files = []
    command = verbose_command_start(f'rglob: {pattern}')
    for file in workdir.rglob(pattern):
        if file.is_file():
            files.append(file)
    verbose_add_map(
        command=command,
        stdout=[],
        stderr=[],
    )
    return files


def search_file_for_check_is_flutter_project(path: Path) -> bool:
    desktop = search_files(path, 'aurora/desktop/*.desktop')
    pubspec = search_files(path, 'pubspec.yaml')
    dart = search_files(path, '*.dart')
    return len(desktop) != 0 and len(dart) != 0 and len(pubspec) != 0


def search_file_for_check_is_aurora_project(path: Path) -> bool:
    desktop = search_files(path, '*.desktop')
    pro = search_files(path, '*.pro')
    qml = search_files(path, '*.qml')
    return len(desktop) != 0 and len(pro) != 0 and len(qml) != 0


def search_aurora_project_builds_rpm(
        path: Path,
        arch: str
) -> []:
    return reversed(search_files(path, f'*{arch}*.rpm'))


def search_project_application_id(path: Path) -> Any:
    desktop = search_files(path, '*.desktop')
    if not desktop:
        return None
    org = ''
    app = ''
    with open(desktop[0]) as f:
        for line in f:
            if 'OrganizationName=' in line:
                org = line.replace('OrganizationName=', '').strip()
            if 'ApplicationName=' in line:
                app = line.replace('ApplicationName=', '').strip()

    if org and app:
        return f'{org}.{app}'
    return None


def search_flutter_project_pubspec_key(
        path: Path,
        key: str
) -> Any:
    pubspec = search_files(path, 'pubspec.yaml')
    if not pubspec:
        return None
    with open(pubspec[0]) as f:
        for line in f:
            if key in line:
                return line
    return None
