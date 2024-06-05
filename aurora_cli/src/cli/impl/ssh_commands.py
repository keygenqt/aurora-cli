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
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.argv import argv_is_test, argv_is_api
from aurora_cli.src.base.utils.output import echo_stdout, OutResult


def ssh_command_common(
        client: SSHClient,
        execute: str,
        verbose: bool
):
    result = ssh_command(
        client=client,
        execute=execute
    )
    if result.is_error():
        echo_stdout(result, verbose)
    else:
        echo_stdout(OutResult(
            message=TextSuccess.ssh_exec_command_success(
                execute=execute,
                stdout='\n'.join(result.value['stdout']),
                stderr='\n'.join(result.value['stderr'])
            ),
            value=result.value
        ), verbose)


def ssh_upload_common(
        client: SSHClient,
        path: [],
        verbose: bool
):
    def state_update(ab: AliveBarPercentage, percent: int):
        if argv_is_api():
            echo_stdout(OutResult(TextInfo.shh_upload_progress(), value=percent))
        else:
            ab.update(percent)

    for file_path in path:
        if not argv_is_test():
            echo_stdout(OutResult(TextInfo.shh_download_start(file_path)))
        bar = AliveBarPercentage()
        echo_stdout(ssh_upload(
            client=client,
            path=file_path,
            listen_progress=lambda stdout: state_update(bar, stdout.value)
        ))
    if verbose:
        echo_stdout(OutResult(), verbose)


def ssh_run_common(
        client: SSHClient,
        package: str,
        verbose: bool,
):
    def echo_stdout_with_check_close(stdout: OutResult | None):
        echo_stdout(stdout)

    result = ssh_run(
        client=client,
        package=package,
        listen_stdout=lambda stdout: echo_stdout_with_check_close(stdout),
        listen_stderr=lambda stderr: echo_stdout(stderr)
    )
    if verbose or result.is_error():
        echo_stdout(result, verbose)


def ssh_install_common(
        client: SSHClient,
        path: [],
        apm: bool,
        verbose: bool,
        devel_su: str | None = None
):
    def state_update(ab: AliveBarPercentage, percent: int):
        if argv_is_api():
            echo_stdout(OutResult(TextInfo.shh_upload_progress(), value=percent))
        else:
            ab.update(percent)
        if percent == 100:
            echo_stdout(OutResult(TextInfo.ssh_install_rpm()))

    for file_path in path:
        echo_stdout(OutResult(TextInfo.shh_download_start(file_path)))
        bar = AliveBarPercentage()
        echo_stdout(ssh_rpm_install(
            client=client,
            path=file_path,
            apm=apm,
            listen_progress=lambda stdout: state_update(bar, stdout.value),
            devel_su=devel_su
        ))
    if verbose:
        echo_stdout(OutResult(), verbose)


def ssh_remove_common(
        client: SSHClient,
        package: str,
        apm: bool,
        verbose: bool,
        devel_su: str | None = None
):
    echo_stdout(ssh_package_remove(
        client=client,
        package=package,
        apm=apm,
        devel_su=devel_su
    ), verbose)
