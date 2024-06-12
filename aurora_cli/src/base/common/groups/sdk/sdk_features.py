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

from aurora_cli.src.base.common.features.load_by_version import (
    get_version_latest_by_url,
    get_download_sdk_url_by_version
)
from aurora_cli.src.base.common.features.request_version import request_versions_sdk
from aurora_cli.src.base.common.features.search_installed import search_installed_sdk
from aurora_cli.src.base.models.sdk_model import SdkModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.disk_cache import disk_cache_clear
from aurora_cli.src.base.utils.download import check_downloads, downloads
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultError
from aurora_cli.src.base.utils.shell import shell_exec_app
from aurora_cli.src.base.utils.url import get_url_version_sdk


def sdk_available_common(verbose: bool):
    echo_stdout(request_versions_sdk(), verbose)


def sdk_installed_common(verbose: bool):
    echo_stdout(search_installed_sdk(), verbose)


def sdk_install_common(
        version: str,
        offline: bool,
        verbose: bool,
        is_bar: bool = True
):
    if SdkModel.get_versions_sdk():
        echo_stdout(OutResultError(TextError.sdk_already_installed_error()), verbose)
        exit(1)

    version_url = get_url_version_sdk(version)
    version_full = get_version_latest_by_url(version_url)
    download_url = get_download_sdk_url_by_version(version_url, version_full)
    urls = [item for item in download_url if (offline and 'offline' in item) or (not offline and 'online' in item)]

    urls, files = check_downloads(urls)

    if not download_url and not files:
        echo_stdout(TextError.get_install_info_error())
        exit(1)

    if urls:
        downloads(urls, verbose, is_bar)

    run = Path(files[0])

    if shell_exec_app(run):
        echo_stdout(OutResult(TextSuccess.shell_run_app_success(run.name)), verbose)
        disk_cache_clear()
    else:
        echo_stdout(OutResultError(TextError.shell_run_app_error(run.name)), verbose)


def sdk_tool_common(model: SdkModel, verbose: bool):
    tool = model.get_tool_path()
    if shell_exec_app(tool):
        echo_stdout(OutResult(TextSuccess.shell_run_app_success(tool.name)), verbose)
        disk_cache_clear()
    else:
        echo_stdout(OutResultError(TextError.shell_run_app_error(tool.name)), verbose)
