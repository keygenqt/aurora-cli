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

from aurora_cli.src.base.constants.url import (
    URL_AURORA_REPO_VERSIONS,
    URL_FLUTTER_SDK_VERSIONS,
    URL_FLUTTER_PLUGINS_VERSIONS
)
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.request import request_get


def _get_versions_from_repo(url: str) -> []:
    from bs4 import BeautifulSoup

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


def request_versions_sdk() -> OutResult:
    try:
        versions = _get_versions_from_repo(URL_AURORA_REPO_VERSIONS)
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_sdk(versions), value=versions)
    except (Exception,):
        return OutResultError(TextError.request_error())


def request_versions_psdk() -> OutResult:
    try:
        versions = _get_versions_from_repo(URL_AURORA_REPO_VERSIONS)
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_psdk(versions), value=versions)
    except (Exception,):
        return OutResultError(TextError.request_error())


def request_versions_flutter() -> OutResult:
    try:
        response = request_get(URL_FLUTTER_SDK_VERSIONS)
        versions = [obj['name'].replace('aurora-', '') for obj in response.json() if not 'debug' in obj['message'].lower()]
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_flutter(versions), value=versions)
    except (Exception,):
        return OutResultError(TextError.request_error())


def request_flutter_plugins() -> OutResult:
    try:
        response = request_get(URL_FLUTTER_PLUGINS_VERSIONS)
        versions = [obj['name'] for obj in response.json()]
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_flutter(versions), value=versions)
    except (Exception,):
        return OutResultError(TextError.request_error())



