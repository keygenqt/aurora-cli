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
from aurora_cli.src.base.common.features.request_version import get_versions_psdk, get_version_latest_by_url, \
    get_download_psdk_url_by_version
from aurora_cli.src.base.common.features.search_installed import search_installed_psdk
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.download import check_downloads, downloads
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.base.utils.url import get_url_version_psdk


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
        echo_stdout(TextError.get_install_info_error())
        exit(1)

    if urls:
        downloads(urls, verbose, is_bar)

    # @todo
    print(files)
