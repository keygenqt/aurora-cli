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

from paramiko.client import SSHClient

from aurora_cli.src.base.common.features.ssh_features import (
    ssh_command,
    ssh_run,
    ssh_upload,
    ssh_rpm_install,
    ssh_package_remove
)
from aurora_cli.src.base.interface.model_client import ModelClient
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.argv import argv_is_test, argv_is_api
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultError
from aurora_cli.src.base.utils.shell import shell_exec_command


def _get_ssh_client(model: ModelClient) -> SSHClient:
    result = model.get_ssh_client()
    if result.is_error():
        echo_stdout(result)
        app_exit()
    return result.value


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
            echo_stdout(OutResult(TextInfo.shh_upload_progress(), value=percent))
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
        debug: bool,
):
    # @todo - Чекнуть по подключение по паролю.
    if debug and model.is_password():
        echo_stdout(OutResultError(TextError.ssh_run_debug_error()))
        app_exit(1)

    client = _get_ssh_client(model)

    def echo_stdout_with_check_close(stdout: OutResult | None):
        if debug and 'The Dart VM service is listening on' in stdout.value:
            url = stdout.value.split(' ')[-1]
            port = url.split('/')[2].split(':')[-1]
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

        echo_stdout(stdout)

    result = ssh_run(
        client=client,
        package=package,
        debug=debug,
        listen_stdout=lambda stdout: echo_stdout_with_check_close(stdout),
        listen_stderr=lambda stderr: echo_stdout(stderr)
    )
    if result.is_error():
        echo_stdout(result)


def ssh_install_common(
        model: ModelClient,
        path: str,
        apm: bool,
        devel_su: str | None = None
):
    client = _get_ssh_client(model)

    def state_update(ab: AliveBarPercentage, percent: int):
        if argv_is_api():
            echo_stdout(OutResult(TextInfo.shh_upload_progress(), value=percent))
        else:
            ab.update(percent)
        if percent == 100:
            echo_stdout(OutResult(TextInfo.ssh_install_rpm()))

    echo_stdout(OutResult(TextInfo.shh_upload_start()))

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
        devel_su: str | None = None
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
