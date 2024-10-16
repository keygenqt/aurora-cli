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
import re
from pathlib import Path
from typing import Any

from aurora_cli.src.base.utils.request import request_get


# Flutter
def get_version_flutter_from_path(file: Path) -> Any:
    path_split = str(file).split('flutter-')
    if len(path_split) == 2:
        path_version = path_split[1].split('/')
        if path_version:
            return path_version[0]
    return None


# PSDK
def get_version_psdk_from_file(file: Path) -> Any:
    with open(file) as f:
        for line in f:
            if 'VERSION_ID=' in line:
                return line.split('=')[1].strip().strip('"')
    return None


def get_tool_psdk_from_file_with_version(file_version: Path) -> Any:
    tool_path = file_version.parent.parent / 'sdk-chroot'
    if tool_path.is_file():
        return tool_path
    return None


# SDK
def get_version_sdk_from_file(file: Path) -> Any:
    with open(file) as f:
        for line in f:
            if 'SDK_RELEASE=' in line:
                return line.split('=')[1].replace('-base', '').strip().strip('"')
    return None


def get_tool_sdk_from_file_with_version(file_version: Path) -> Any:
    tool_path = file_version.parent / 'SDKMaintenanceTool'
    if tool_path.is_file():
        return tool_path
    return None


def get_run_sdk_from_file_with_version(file_version: Path) -> Any:
    tool_path = file_version.parent / 'bin' / 'qtcreator.sh'
    if tool_path.is_file():
        return tool_path
    return None


# PSDK / SDK
def get_version_latest_by_url_custom_5_1(url: str) -> []:
    from bs4 import BeautifulSoup

    root_url = '/'.join(url.split('/')[:-2])
    versions = []
    response = request_get(root_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.strip('/')
            if re.search(r'^\d+\.\d+\.\d+', text):
                if 'PlatformSDK' in url:
                    versions.append(f'{root_url}/{text}/PlatformSDK/')
                else:
                    versions.append(f'{root_url}/{text}/AuroraSDK-base/')
    return versions


def get_version_latest_by_url(major: str, url: str) -> Any:
    from bs4 import BeautifulSoup

    urls = []

    if '5.1' in url:
        urls = get_version_latest_by_url_custom_5_1(url)

    response = request_get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.strip('/')
            if re.search(r'^\d+\.\d+\.\d+', text):
                urls.append(f'{url}{text}/')

    minor = []

    for value in urls:
        matches = re.findall(r'\d+\.\d+\.\d+\.\d+', value)
        if matches:
            minor.append(int(matches[0].split('.')[-1]))

    if minor:
        minor = sorted(minor)[-1]
        for value in urls:
            version = f'{major}.{minor}'
            if version in value:
                return version, value

    return None, None


def get_download_sdk_url_by_version(url: str) -> []:
    from bs4 import BeautifulSoup

    urls = []
    response = request_get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.strip('/')
            if re.search(r'.run$', text) and 'testing' not in text:
                urls.append(f'{url}{text}')
    return urls


def get_download_psdk_url_by_version(url: str) -> []:
    from bs4 import BeautifulSoup

    urls = []
    response = request_get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.strip('/')
            if re.search(r'.tar.(bz2|7z)$', text) and 'pu-' not in text:
                urls.append(f'{url}{text}')
    return urls
