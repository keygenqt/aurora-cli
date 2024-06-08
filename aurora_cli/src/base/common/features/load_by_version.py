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


# Flutter
def get_version_flutter_from_path(file: Path) -> str | None:
    path_split = str(file).split('flutter-')
    if len(path_split) == 2:
        path_version = path_split[1].split('/')
        if path_version:
            return path_version[0]
    return None


# PSDK
def get_version_psdk_from_file(file: Path) -> str | None:
    with open(file) as f:
        for line in f:
            if 'PRETTY_NAME=' in line:
                return line.split('=')[1].strip().strip('"')
    return None


def get_tool_psdk_from_file_with_version(file_version: Path) -> Path | None:
    tool_path = file_version.parent.parent / 'sdk-chroot'
    if tool_path.is_file():
        return tool_path
    return None


# SDK
def get_version_sdk_from_file(file: Path) -> str | None:
    with open(file) as f:
        for line in f:
            if 'SDK_RELEASE=' in line:
                return line.split('=')[1].replace('-base', '').strip().strip('"')
    return None


def get_tool_sdk_from_file_with_version(file_version: Path) -> Path | None:
    tool_path = file_version.parent / 'SDKMaintenanceTool'
    if tool_path.is_file():
        return tool_path
    return None
