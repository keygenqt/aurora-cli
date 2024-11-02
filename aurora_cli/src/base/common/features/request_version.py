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

from packaging.version import Version

from aurora_cli.src.base.constants.url import (
    URL_AURORA_REPO_VERSIONS,
    URL_FLUTTER_SDK_VERSIONS,
    URL_FLUTTER_PLUGINS_VERSIONS
)
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.request import request_get


def _get_list_versions_from_repo() -> []:
    from bs4 import BeautifulSoup

    # Search first level
    levels1 = []
    response = request_get(URL_AURORA_REPO_VERSIONS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.replace('/', '')
            if not '..' in text and re.search(r'\d.\d.\d', text) and not '4.0.1' in text:
                levels1.append(f'{URL_AURORA_REPO_VERSIONS}{text}')

    # Search second level
    levels2 = []
    for level1 in levels1:
        response = request_get(level1)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.findAll('a'):
                text = item.text.replace('/', '')
                if not '..' in text and text in ['AppSDK', 'PlatformSDK'] or '-release' in text:
                    levels2.append(f'{level1}/{text}')

    # Search second level
    data = []
    versions = []
    for level2 in levels2:
        response = request_get(level2)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.findAll('a'):
                text = item.text.replace('/', '')
                if not '..' in text and (
                        re.search(r'^\d.\d.\d', text) or text in ['AuroraPSDK', 'PlatformSDK', 'AuroraSDK-base',
                                                                  'AuroraSDK-MB2']):
                    url = f'{level2}/{text}'
                    full_version = [v.replace('-release', '') for v in url.split('/') if
                                    re.search(r'^\d.\d.\d.\d', v) or '-release' in v][0]
                    is_psdk = True if 'AuroraPSDK' in url or 'PlatformSDK' in url else False
                    versions.append(full_version)
                    data.append({
                        'url': url,
                        'version': full_version,
                        'is_psdk': is_psdk,
                    })
    # Sort versions
    versions = list(set(versions))
    versions.sort(key=Version)
    versions.reverse()

    # Sort data
    sort_data = []
    for v in versions:
        for d in data:
            if v == d['version']:
                sort_data.append(d)

    return sort_data


def get_versions_sdk() -> []:
    return [v['version'] for v in _get_list_versions_from_repo() if not v['is_psdk']]


def get_versions_psdk() -> []:
    return [v['version'] for v in _get_list_versions_from_repo() if v['is_psdk']]


def get_version_sdk_url(version):
    version = [v['url'] for v in _get_list_versions_from_repo() if version == v['version'] and not v['is_psdk']]
    return version[0] if version else None


def get_version_psdk_url(version):
    version = [v['url'] for v in _get_list_versions_from_repo() if version == v['version'] and v['is_psdk']]
    return version[0] if version else None


def request_versions_sdk() -> OutResult:
    try:
        versions = get_versions_sdk()
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_sdk(versions), value=versions)
    except (Exception,):
        return OutResultError(TextError.request_error())


def request_versions_psdk() -> OutResult:
    try:
        versions = get_versions_psdk()
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_psdk(versions), value=versions)
    except (Exception,):
        return OutResultError(TextError.request_error())


def request_versions_flutter() -> OutResult:
    try:
        response = request_get(URL_FLUTTER_SDK_VERSIONS)
        versions = [obj['name'].replace('aurora-', '') for obj in response.json() if
                    not 'debug' in obj['message'].lower()]
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
