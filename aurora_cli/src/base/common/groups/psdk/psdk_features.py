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

import signal
import subprocess
from pathlib import Path
from time import sleep

from grapheme.grapheme_property_group import value

from aurora_cli.src.base.common.features.load_by_version import (
    get_version_latest_by_url,
    get_download_psdk_url_by_version
)
from aurora_cli.src.base.common.features.request_version import request_versions_psdk
from aurora_cli.src.base.common.features.search_installed import search_installed_psdk
from aurora_cli.src.base.common.features.shell_features import (
    shell_psdk_targets,
    shell_tar_sudo_unpack,
    shell_psdk_tooling_create,
    shell_psdk_target_create,
    shell_remove_root_folder,
    shell_psdk_clear,
)
from aurora_cli.src.base.common.groups.psdk.psdk_sudoers_features import psdk_is_sudoers
from aurora_cli.src.base.localization.localization import localization_abort_start, localization_abort_end
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.workdir_model import WorkdirModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_exit, app_abort_handler
from aurora_cli.src.base.utils.argv import argv_is_api
from aurora_cli.src.base.utils.cache_func import cache_func_clear
from aurora_cli.src.base.utils.download import check_downloads, downloads
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResultInfo, OutResult
from aurora_cli.src.base.utils.tests import tests_exit
from aurora_cli.src.base.utils.text_file import file_remove_line
from aurora_cli.src.base.utils.url import get_url_version_psdk


def psdk_info_common(model: PsdkModel):
    echo_stdout(OutResult(value={
        'VERSION': model.version,
        'TOOL': f'{model.tool}',
        'SUDOERS': psdk_is_sudoers(model)
    }))


def psdk_available_common():
    echo_stdout(request_versions_psdk())


def psdk_installed_common():
    echo_stdout(search_installed_psdk())


def psdk_targets_common(
        model: PsdkModel,
        password = None
):
    echo_stdout(shell_psdk_targets(model.get_tool_path(), model.get_version(), password))


def psdk_install_common(
        version: str,
        is_bar: bool = True,
        mode: str = None,
        password = None
):
    tests_exit()
    # url major version
    version_url = get_url_version_psdk(version)
    # get full latest version and url
    version_full, version_url_latest = get_version_latest_by_url(version, version_url)

    if not version_url_latest:
        echo_stdout(OutResultError(TextError.repo_search_error()))
        app_exit()

    # get url path to files
    urls = get_download_psdk_url_by_version(version_url_latest)

    # check already exists
    versions = PsdkModel.get_versions_psdk()
    if version_full in versions:
        echo_stdout(OutResultError(TextError.psdk_already_installed_error(version_full)))
        app_exit()

    # check download urls
    urls, files = check_downloads(urls)

    if not urls and not files:
        echo_stdout(OutResultError(TextError.get_install_info_error()))
        app_exit()

    if mode == 'download' or mode is None:
        _psdk_install_download(urls, is_bar)

    if mode == 'install' or mode is None:
        _psdk_install(files, version_full, is_bar, password)


def _psdk_install_download(
        urls: [],
        is_bar: bool = True
):
    if urls:
        echo_stdout(OutResultInfo(TextInfo.psdk_download_start()))
        downloads(urls, is_bar)
        sleep(1)


def _psdk_install(
        files: [],
        version_full: str,
        is_bar: bool = True,
        password = None
):
    # Create folders
    workdir = WorkdirModel.get_workdir()
    psdk_path = workdir / f'AuroraPlatformSDK-{version_full}'
    psdk_dir = psdk_path / 'sdks' / 'aurora_psdk'
    toolings = psdk_path / 'toolings'
    tarballs = psdk_path / 'tarballs'
    targets = psdk_path / 'targets'
    tool = psdk_dir / 'sdk-chroot'

    path_chroot = [str(file) for file in files if 'Chroot' in str(file)]
    path_tooling = [str(file) for file in files if 'Tooling' in str(file)]
    path_targets = [str(file) for file in files if 'Target' in str(file)]

    if not path_chroot or not path_tooling or not path_targets:
        echo_stdout(OutResultError(TextError.get_install_info_error()))
        app_exit()

    psdk_path.mkdir(parents=True, exist_ok=True)
    psdk_dir.mkdir(parents=True, exist_ok=True)
    toolings.mkdir(parents=True, exist_ok=True)
    tarballs.mkdir(parents=True, exist_ok=True)
    targets.mkdir(parents=True, exist_ok=True)

    bar = AliveBarPercentage()

    # Ignore ctrl-c
    def exec_fn():
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def out_progress(percent: int, title: str):
        if is_bar:
            bar.update(percent, title, 16)
        else:
            echo_stdout(OutResultInfo(title, value=percent))

    def abort():
        bar.stop()
        localization_abort_start()
        if password:
            subprocess.call(
                ['echo', password, '|', 'sudo', '-S'] + ['rm', '-rf', str(psdk_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=exec_fn
            )
        else:
            subprocess.call(
                ['sudo', 'rm', '-rf', str(psdk_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=exec_fn
            )
        localization_abort_end()
        exit(0)

    app_abort_handler(lambda: abort())

    echo_stdout(OutResultInfo(TextInfo.psdk_install_start(), value=1))

    if not password:
        subprocess.call(['sudo', 'echo'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    echo_stdout(shell_tar_sudo_unpack(
        archive_path=path_chroot[0],
        unpack_path=str(psdk_dir),
        progress=lambda percent: out_progress(percent, 'Platform Chroot'),
        password=password
    ))

    if argv_is_api():
        sleep(1)

    echo_stdout(shell_psdk_tooling_create(
        tool=str(tool),
        version=version_full,
        path=path_tooling[0],
        progress=lambda percent: out_progress(percent, 'Platform Tooling'),
        password=password
    ))

    if argv_is_api():
        sleep(1)

    for path_target in path_targets:
        arch = path_target.split('-')[-1].split('.')[0]
        echo_stdout(shell_psdk_target_create(
            tool=str(tool),
            version=version_full,
            path=str(path_target),
            arch=arch,
            progress=lambda percent: out_progress(percent, f'Target {arch}'),
            password=password
        ))

    if argv_is_api():
        sleep(1)

    cache_func_clear()
    echo_stdout(OutResult(TextSuccess.psdk_install_success(str(psdk_path), version_full)))


def psdk_remove_common(
        model: PsdkModel,
        password = None
):
    tests_exit()
    echo_stdout(OutResultInfo(TextInfo.psdk_remove_start()))
    result = shell_remove_root_folder(model.get_path(), password)
    if result.is_error():
        echo_stdout(result)
        app_exit()
    file_remove_line(Path.home() / '.bashrc', model.get_path())
    cache_func_clear()
    echo_stdout(OutResult(TextSuccess.psdk_remove_success(model.get_version())))


def psdk_clear_common(
        model: PsdkModel,
        target: str,
        password = None
):
    tests_exit()
    echo_stdout(shell_psdk_clear(model.get_tool_path(), target, password))
