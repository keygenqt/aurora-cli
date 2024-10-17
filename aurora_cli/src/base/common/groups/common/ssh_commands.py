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
from time import sleep
from typing import Any

from paramiko.client import SSHClient

from aurora_cli.src.base.common.features.search_files import (
    search_file_for_check_is_flutter_project,
    search_file_for_check_is_aurora_project
)
from aurora_cli.src.base.common.features.shell_vscode import (
    update_launch_debug_gdb,
    update_launch_debug_dart,
)
from aurora_cli.src.base.common.features.ssh_features import (
    ssh_command,
    ssh_run,
    ssh_upload,
    ssh_rpm_install,
    ssh_package_remove,
    ssh_download,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.interface.model_client import ModelClient
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.hint import TextHint
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.argv import argv_is_test, argv_is_api
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultError, OutResultInfo
from aurora_cli.src.base.utils.path import path_convert_relative
from aurora_cli.src.base.utils.shell import shell_exec_command
from aurora_cli.src.base.utils.tests import tests_exit


def _get_ssh_client(model: ModelClient) -> SSHClient:
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result)
        app_exit()
    return result.value


def ssh_info_common(
        model: ModelClient,
        is_emulator
):
    client = _get_ssh_client(model)

    if is_emulator:
        result = ssh_command(
            client=client,
            execute="cat /etc/os-release"
        )
    else:
        result = ssh_command(
            client=client,
            execute="cat /etc/rpm/platform && echo '\n' && cat /etc/os-release"
        )

    if result.is_error():
        echo_stdout(result)
        return

    info = {}

    if is_emulator:
        info['ARCH'] = 'x86_64'

    for line in result.value['stdout']:
        if '=' not in line:
            info['ARCH'] = 'armv7hl' if 'armv7hl' in line else 'aarch64'
        else:
            data = line.split('=')
            info[data[0]] = data[1].strip('"')

    info['HOST'] = model.get_host()
    info['PORT'] = model.get_port()
    if model.is_password():
        info['PASS'] = str(model.get_pass())
    else:
        info['KEY'] = str(model.get_ssh_key())

    echo_stdout(OutResult(value=info))


def ssh_command_common(
        model: ModelClient,
        execute: str,
):
    client = _get_ssh_client(model)
    result = ssh_command(
        client=client,
        execute=execute
    )
    if result.is_error():
        echo_stdout(result)
    else:
        echo_stdout(OutResult(
            message=TextSuccess.ssh_exec_command_success(
                execute=execute,
                stdout='\n'.join(result.value['stdout']),
                stderr='\n'.join(result.value['stderr'])
            ),
            value=result.value
        ))


def ssh_upload_common(
        model: ModelClient,
        path: str,
):
    client = _get_ssh_client(model)

    def state_update(ab: AliveBarPercentage, percent: int):
        if argv_is_api():
            echo_stdout(OutResultInfo(TextInfo.shh_upload_progress(), value=percent))
            if percent == 100:
                sleep(1) # show 100%
        else:
            ab.update(percent)

    if not argv_is_test():
        echo_stdout(OutResult(TextInfo.shh_upload_start()))

    bar = AliveBarPercentage()

    echo_stdout(ssh_upload(
        client=client,
        path=path,
        listen_progress=lambda stdout: state_update(bar, stdout.value),
    ))


def ssh_run_common(
        model: ModelClient,
        package: str,
        run_mode: str,  # dart/gdb/sandbox
        path_project: str
):
    tests_exit()

    if run_mode != 'sandbox' and model.is_password():
        echo_stdout(OutResultError(TextError.ssh_run_debug_error()))
        app_exit()

    client = _get_ssh_client(model)
    project = path_convert_relative(path_project)
    is_project_flutter = search_file_for_check_is_flutter_project(project)
    is_project_aurora = search_file_for_check_is_aurora_project(project)

    if is_project_aurora:
        echo_stdout(OutResultInfo(TextInfo.ssh_run_debug_aurora()))

    if run_mode == 'gdb':
        download_bin_path_result = ssh_download(
            path_remote=f'/usr/bin/{package}',
            path_local=f'{AppConfig.get_tempdir()}/{package}',
            client=client,
            force=True,
            close=False
        )
        if download_bin_path_result.is_error():
            echo_stdout(download_bin_path_result)
        else:
            if is_project_flutter:
                update_launch_debug_gdb(
                    host=model.get_host(),
                    binary=download_bin_path_result.value['localpath'],
                    package=package,
                    project=project,
                )
                echo_stdout(OutResultInfo(TextInfo.update_launch_json_gdb()))
                echo_stdout(OutResultInfo(TextHint.custom_devices()))
            else:
                echo_stdout(OutResultInfo(TextInfo.ssh_debug_without_project_gdb(
                    binary=download_bin_path_result.value['localpath'],
                    host=model.get_host(),
                    package=package,
                )))

    def forward_port(port):
        _stdout, _stderr = shell_exec_command([
            'ssh',
            '-i',
            str(model.get_ssh_key()),
            '-NfL',
            f'{port}:127.0.0.1:{port}',
            f'defaultuser@{model.get_host()}',
            f'-p{model.get_port()}'
        ])
        if _stdout and '@@@@@@@@@' in _stdout[0]:
            echo_stdout(OutResultError(TextError.ssh_forward_port_error()))
        else:
            echo_stdout(OutResult(TextSuccess.ssh_forward_port_success()))

    def echo_stdout_with_check_close(stdout: Any):

        if run_mode == 'gdb' and 'Listening on port' in stdout.value:
            port = stdout.value.split(' ')[-1]
            forward_port(port)
            echo_stdout(OutResult(TextSuccess.ssh_gdb_server_start_success()))

        if run_mode == 'dart' and 'The Dart VM service is listening on' in stdout.value:
            url = stdout.value.split(' ')[-1]
            port = url.split('/')[2].split(':')[-1]
            forward_port(port)

            if is_project_flutter:
                update_launch_debug_dart(
                    url=url,
                    project=project,
                )
                echo_stdout(OutResultInfo(TextInfo.update_launch_json_dart()))
                echo_stdout(OutResultInfo(TextHint.custom_devices()))
            else:
                echo_stdout(OutResultInfo(TextInfo.ssh_debug_without_project_dart(url)))

        echo_stdout(stdout)

    result = ssh_run(
        client=client,
        package=package,
        run_mode=run_mode,
        listen_stdout=lambda stdout: echo_stdout_with_check_close(stdout),
        listen_stderr=lambda stderr: echo_stdout(stderr)
    )
    if result.is_error():
        echo_stdout(result)


def ssh_install_common(
        model: ModelClient,
        path: str,
        apm: bool,
        devel_su: Any = None
):
    client = _get_ssh_client(model)

    def state_update(ab: AliveBarPercentage, percent: int):
        if argv_is_api():
            echo_stdout(OutResultInfo(TextInfo.shh_upload_progress(), value=percent))
            if percent == 100:
                sleep(1)  # show 100%
        else:
            ab.update(percent)
        if percent == 100:
            echo_stdout(OutResultInfo(TextInfo.ssh_start_install_rpm()))

    echo_stdout(OutResultInfo(TextInfo.shh_upload_start()))

    bar = AliveBarPercentage()

    result = ssh_rpm_install(
        client=client,
        path=path,
        apm=apm,
        listen_progress=lambda stdout: state_update(bar, stdout.value),
        devel_su=devel_su
    )

    echo_stdout(result)
    if result.is_error():
        app_exit()


def ssh_remove_common(
        model: ModelClient,
        package: str,
        apm: bool,
        devel_su: Any = None
):
    client = _get_ssh_client(model)

    echo_stdout(ssh_package_remove(
        client=client,
        package=package,
        apm=apm,
        devel_su=devel_su
    ))


def ssh_check_package(
        model: ModelClient,
        package: str,
) -> bool:
    client = _get_ssh_client(model)
    result = ssh_command(
        client=client,
        execute=f'ls /usr/bin/{package}'
    )
    client.close()
    return 'No such file or directory' not in result.value['stdout'][0]
