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

import requests
from requests import Response

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import OutResult, OutResultError, OutResultInfo
from aurora_cli.src.base.utils.path import path_get_download_path
from aurora_cli.src.base.utils.verbose import verbose_add_map


def request_get(url: str, stream: bool = False) -> Response | OutResult:
    try:
        response = requests.get(url, stream=stream)
        verbose_add_map(
            command=f'request: {url}',
            stdout=[response.text],
            stderr=[],
        )
        return response
    except Exception as e:
        verbose_add_map(
            command=f'request: {url}',
            stdout=[],
            stderr=[str(e)],
        )
        return OutResultError(TextError.request_error())


def request_check_url_download(url: str) -> OutResult:
    download = path_get_download_path(url)
    response = requests.head(url)
    response_length = int(response.headers.get('content-length'))
    if not response_length or response.status_code != 200:
        return OutResultError(TextError.check_url_download_error(url))

    if download.is_dir():
        return OutResultError(TextError.check_url_download_dir_error(str(download)))

    if download.is_file():
        if download.stat().st_size == response_length:
            return OutResultInfo(TextInfo.check_url_download_exist(str(download)), value=str(download))
        else:
            return OutResultError(TextError.check_url_download_exist_error(str(download)))

    return OutResult(TextSuccess.check_url_download_success(), value=str(download))
