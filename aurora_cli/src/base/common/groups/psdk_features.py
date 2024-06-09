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

from aurora_cli.src.base.common.features.request_version import (
    get_versions_psdk,
    get_version_latest_by_url,
    get_download_psdk_url_by_version
)
from aurora_cli.src.base.common.features.search_installed import search_installed_psdk
from aurora_cli.src.base.common.features.shell_features import shell_resign
from aurora_cli.src.base.constants.app import PATH_REGULAR_KEY, PATH_REGULAR_CERT
from aurora_cli.src.base.constants.url import URL_REGULAR_KEY, URL_REGULAR_CERT
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.disk_cache import disk_cache_clear
from aurora_cli.src.base.utils.download import check_downloads, downloads, check_with_download_files
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResultInfo, OutResult
from aurora_cli.src.base.utils.url import get_url_version_psdk


def _get_open_keys(verbose: bool, is_bar: bool) -> [Path]:
    return check_with_download_files(
        files=[PATH_REGULAR_KEY, PATH_REGULAR_CERT],
        urls=[URL_REGULAR_KEY, URL_REGULAR_CERT],
        verbose=verbose,
        is_bar=is_bar
    )


def psdk_available_common(verbose: bool):
    echo_stdout(get_versions_psdk(), verbose)


def psdk_installed_common(verbose: bool):
    echo_stdout(search_installed_psdk(), verbose)


def psdk_install_common(
        version: str,
        verbose: bool,
        is_bar: bool = True
):
    # url major version
    version_url = get_url_version_psdk(version)
    # get full latest version
    version_full = get_version_latest_by_url(version_url)
    # get url path to files
    urls = get_download_psdk_url_by_version(version_url, version_full)

    # check download urls
    urls, files = check_downloads(urls)

    if not urls and not files:
        echo_stdout(OutResultError(TextError.get_install_info_error()), verbose)
        exit(1)

    if urls:
        downloads(urls, verbose, is_bar)

    # @todo
    print(files)

    # clear cache
    disk_cache_clear()


def psdk_remove_common(model: PsdkModel):
    print('Coming soon')


def psdk_clear_common(model: PsdkModel):
    print('Coming soon')


def psdk_package_search_common(model: PsdkModel, package: str):
    print('Coming soon')


def psdk_package_install_common(model: PsdkModel, path: []):
    print('Coming soon')


def psdk_package_remove_common(model: PsdkModel, package: str):
    print('Coming soon')


def psdk_sign_common(
        model_psdk: PsdkModel,
        model_keys: SignModel | None,
        paths: [str],
        verbose: bool,
        is_bar: bool = True
):
    if not model_keys:
        echo_stdout(OutResultInfo(TextInfo.psdk_sign_use_public_keys()))
        keys = _get_open_keys(verbose, is_bar)
        model_keys = SignModel('_', keys[0], keys[1])

    result = shell_resign(
        tool=model_psdk.get_tool_path(),
        key=str(model_keys.key),
        cert=str(model_keys.cert),
        paths=paths
    )

    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)

    echo_stdout(OutResult(TextSuccess.psdk_sign_success()), verbose)


def psdk_sudoers_add_common(model: PsdkModel):
    print('Coming soon')


def psdk_sudoers_remove_common(model: PsdkModel):
    print('Coming soon')


def psdk_targets_common(model: PsdkModel):
    print('Coming soon')


def psdk_validate_common(
        model: PsdkModel,
        path: [],
        profile: str
):
    print('Coming soon')
