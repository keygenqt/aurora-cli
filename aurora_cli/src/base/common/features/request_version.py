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

from bs4 import BeautifulSoup

from aurora_cli.src.base.constants.url import URL_AURORA_REPO_VERSIONS, URL_FLUTTER_SDK_VERSIONS, \
    URL_FLUTTER_PLUGINS_VERSIONS
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.request import request_get


def get_versions_from_repo(url: str) -> []:
    versions = []
    response = request_get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.replace('/', '')
            if re.search(r'\d.\d.\d', text):
                versions.append(text)
    versions.reverse()
    return versions


def get_versions_sdk() -> OutResult:
    try:
        versions = get_versions_from_repo(URL_AURORA_REPO_VERSIONS)
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_sdk(versions), value={'versions': versions})
    except (Exception,):
        return OutResultError(TextError.request_error())


def get_versions_psdk() -> OutResult:
    try:
        versions = get_versions_from_repo(URL_AURORA_REPO_VERSIONS)
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_psdk(versions), value={'versions': versions})
    except (Exception,):
        return OutResultError(TextError.request_error())


def get_versions_flutter() -> OutResult:
    try:
        response = request_get(URL_FLUTTER_SDK_VERSIONS)
        versions = [obj['name'] for obj in response.json()]
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_flutter(versions))
    except (Exception,):
        return OutResultError(TextError.request_error())


def get_flutter_plugins() -> OutResult:
    try:
        response = request_get(URL_FLUTTER_PLUGINS_VERSIONS)
        versions = [obj['name'] for obj in response.json()]
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_flutter(versions))
    except (Exception,):
        return OutResultError(TextError.request_error())


def get_version_latest_by_url(url: str) -> []:
    major = ''
    versions = []
    response = request_get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.strip('/')
            if re.search(r'^\d.\d.\d', text):
                version = int(text.split('.')[-1])
                major = text.replace(str(version), '')
                versions.append(version)
    if versions:
        return f'{major}{sorted(versions)[-1]}'
    return versions


def get_download_url_by_version(url: str, version: str) -> []:
    urls = []
    response = request_get(f'{url}{version}')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.strip('/')
            if re.search(r'.run$', text) and 'testing' not in text:
                urls.append(f'{url}{version}/{text}')
    return urls
