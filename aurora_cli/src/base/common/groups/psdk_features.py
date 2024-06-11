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
import getpass
import signal
import subprocess
from pathlib import Path
from time import sleep

from aurora_cli.src.base.common.features.load_by_version import (
    get_version_latest_by_url,
    get_download_psdk_url_by_version
)
from aurora_cli.src.base.common.features.request_version import request_versions_psdk
from aurora_cli.src.base.common.features.search_installed import search_installed_psdk
from aurora_cli.src.base.common.features.shell_features import (
    shell_psdk_resign,
    shell_psdk_targets,
    shell_psdk_package_search,
    shell_psdk_package_install,
    shell_psdk_package_validate,
    shell_psdk_package_remove,
    shell_psdk_snapshot_remove,
    shell_tar_sudo_unpack,
    shell_psdk_tooling_create,
    shell_psdk_target_create,
    shell_remove_root_folder,
)
from aurora_cli.src.base.constants.app import PATH_REGULAR_KEY, PATH_REGULAR_CERT
from aurora_cli.src.base.constants.other import (
    MER_SDK_CHROOT_PATH,
    SDK_CHROOT_PATH,
    MER_SDK_CHROOT_DATA,
    SDK_CHROOT_DATA
)
from aurora_cli.src.base.constants.url import URL_REGULAR_KEY, URL_REGULAR_CERT
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.models.workdir_model import WorkdirModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.abort import abort_catch
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.disk_cache import disk_cache_clear
from aurora_cli.src.base.utils.download import check_downloads, downloads, check_with_download_files
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResultInfo, echo_stdout_verbose, OutResult
from aurora_cli.src.base.utils.shell import shell_exec_command
from aurora_cli.src.base.utils.text_file import (
    file_exist_in_line,
    file_permissions_777,
    file_permissions_644,
    file_remove_line
)
from aurora_cli.src.base.utils.url import get_url_version_psdk


def _get_open_keys(verbose: bool, is_bar: bool) -> [Path]:
    return check_with_download_files(
        files=[PATH_REGULAR_KEY, PATH_REGULAR_CERT],
        urls=[URL_REGULAR_KEY, URL_REGULAR_CERT],
        verbose=verbose,
        is_bar=is_bar
    )


def psdk_available_common(verbose: bool):
    echo_stdout(request_versions_psdk(), verbose)


def psdk_installed_common(verbose: bool):
    echo_stdout(search_installed_psdk(), verbose)


def psdk_targets_common(model: PsdkModel, verbose: bool):
    result = shell_psdk_targets(model.get_tool_path(), model.get_version())
    echo_stdout(result, verbose)


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

    # check already exists
    versions = PsdkModel.get_versions_psdk()
    if version_full in versions:
        echo_stdout(OutResultError(TextError.psdk_already_installed_error(version_full)), verbose)
        exit(1)

    # check download urls
    urls, files = check_downloads(urls)

    if not urls and not files:
        echo_stdout(OutResultError(TextError.get_install_info_error()), verbose)
        exit(1)

    if urls:
        echo_stdout(OutResultInfo(TextInfo.psdk_download_start()))
        downloads(urls, verbose, is_bar)
        sleep(1)

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
        echo_stdout(OutResultError(TextError.get_install_info_error()), verbose)
        exit(1)

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
            echo_stdout(OutResultInfo(TextInfo.install_progress(), value=percent))

    def abort():
        bar.stop()
        subprocess.call(
            ['sudo', 'rm', '-rf', str(psdk_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=exec_fn
        )
        exit(0)

    abort_catch(lambda: abort())

    echo_stdout(OutResultInfo(TextInfo.psdk_install_start()))

    echo_stdout(shell_tar_sudo_unpack(
        archive_path=path_chroot[0],
        unpack_path=str(psdk_dir),
        progress=lambda percent: out_progress(percent, 'Platform Chroot')
    ))

    echo_stdout(shell_psdk_tooling_create(
        tool=str(tool),
        version=version_full,
        path=path_tooling[0],
        progress=lambda percent: out_progress(percent, 'Platform Tooling')
    ))

    for path_target in path_targets:
        arch = path_target.split('-')[-1].split('.')[0]
        echo_stdout(shell_psdk_target_create(
            tool=str(tool),
            version=version_full,
            path=str(path_target),
            arch=arch,
            progress=lambda percent: out_progress(percent, f'Target {arch}')
        ))

    disk_cache_clear()

    echo_stdout(OutResult(TextSuccess.psdk_install_success(str(psdk_path), version_full)), verbose)


def psdk_remove_common(model: PsdkModel, verbose: bool):
    echo_stdout(OutResultInfo(TextInfo.psdk_remove_start()))
    result = shell_remove_root_folder(model.get_path())
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    file_remove_line(Path.home() / '.bashrc', model.get_path())
    disk_cache_clear()
    echo_stdout(OutResult(TextSuccess.psdk_remove_success(model.get_version())), verbose)


def psdk_snapshot_remove_common(
        model: PsdkModel,
        target: str,
        verbose: bool
):
    result = shell_psdk_snapshot_remove(model.get_tool_path(), target)
    echo_stdout(result, verbose)


def psdk_package_search_common(
        model: PsdkModel,
        target: str,
        package: str,
        verbose: bool
):
    result = shell_psdk_package_search(model.get_tool_path(), target, package)
    echo_stdout(result, verbose)


def psdk_package_install_common(
        model: PsdkModel,
        target: str,
        path: str,
        verbose: bool
):
    result = shell_psdk_package_install(model.get_tool_path(), target, path)
    echo_stdout(result, verbose)


def psdk_package_remove_common(
        model: PsdkModel,
        target: str,
        package: str,
        verbose: bool
):
    result = shell_psdk_package_remove(model.get_tool_path(), target, package)
    echo_stdout(result, verbose)


def psdk_package_validate_common(
        model: PsdkModel,
        target: str,
        path: str,
        profile: str,
        verbose: bool
):
    result = shell_psdk_package_validate(model.get_tool_path(), target, path, profile)
    echo_stdout(result, verbose)


def psdk_package_sign_common(
        model_psdk: PsdkModel,
        model_keys: SignModel | None,
        path: str,
        verbose: bool,
        is_bar: bool = True
):
    if not model_keys:
        echo_stdout(OutResultInfo(TextInfo.psdk_sign_use_public_keys()))
        keys = _get_open_keys(verbose, is_bar)
        model_keys = SignModel('_', keys[0], keys[1])

    result = shell_psdk_resign(
        tool=model_psdk.get_tool_path(),
        key=str(model_keys.key),
        cert=str(model_keys.cert),
        path=path
    )

    echo_stdout(result, verbose)


def psdk_sudoers_add_common(model: PsdkModel, verbose: bool):
    for item in [[MER_SDK_CHROOT_PATH, MER_SDK_CHROOT_DATA], [SDK_CHROOT_PATH, SDK_CHROOT_DATA]]:
        path = Path(item[0])
        tool = Path(model.get_tool_path())
        user = getpass.getuser()
        data = item[1].format(username=user, psdk_tool=tool, psdk_tool_folder=tool.parent)
        if not path.is_file():
            shell_exec_command(['sudo', 'touch', str(path)])
        if file_exist_in_line(path, str(tool.parent)):
            echo_stdout(TextInfo.psdk_sudoers_exist(model.version, str(path)))
        else:
            file_permissions_777(path)
            with open(path, 'a') as file:
                file.write(data)
            file_permissions_644(path)
            echo_stdout(TextSuccess.psdk_sudoers_add_success(model.version, str(path)))

    echo_stdout_verbose(verbose)


def psdk_sudoers_remove_common(model: PsdkModel, verbose: bool):
    for path in [MER_SDK_CHROOT_PATH, SDK_CHROOT_PATH]:
        path = Path(path)
        tool = Path(model.get_tool_path())
        if not path.is_file():
            echo_stdout(TextInfo.psdk_sudoers_not_found(model.version, str(path)))
            continue
        if not file_exist_in_line(path, str(tool.parent)):
            echo_stdout(TextInfo.psdk_sudoers_not_found(model.version, str(path)))
            continue
        file_permissions_777(path)
        file_remove_line(path, str(tool.parent))
        file_permissions_644(path)
        echo_stdout(TextSuccess.psdk_sudoers_remove_success(model.version, str(path)))

    echo_stdout_verbose(verbose)
