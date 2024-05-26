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

from aurora_cli.src.base.common.ssh_features import (
    ssh_command,
    ssh_run,
    ssh_upload,
    ssh_rpm_install,
    ssh_package_remove
)
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout, OutResult


def ssh_common_command_cli(
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
            )
        ), verbose)


def ssh_common_run_cli(
        client: SSHClient,
        package: str,
        nohup: bool,
        verbose: bool,
):
    def echo_stdout_with_check_close(stdout: OutResult | None):
        if stdout and nohup and not stdout.is_error() and 'nohup:' in stdout.value:
            echo_stdout(OutResult(TextSuccess.ssh_run_package(package)))
        else:
            echo_stdout(stdout)

    echo_stdout(ssh_run(
        client=client,
        package=package,
        nohup=nohup,
        listen_stdout=lambda stdout: echo_stdout_with_check_close(stdout),
        listen_stderr=lambda stderr: echo_stdout(stderr)
    ), verbose)


def ssh_common_upload_cli(
        client: SSHClient,
        path: [],
        verbose: bool
):
    for file_path in path:
        if not argv_is_test():
            echo_stdout(TextInfo.shh_download_start(file_path))
        bar = AliveBarPercentage()
        echo_stdout(ssh_upload(
            client=client,
            path=file_path,
            listen_progress=lambda stdout: bar.update(stdout.value)
        ))
    if verbose:
        echo_stdout(OutResult(), verbose)


def ssh_common_install_cli(
        client: SSHClient,
        path: [],
        apm: bool,
        verbose: bool,
        devel_su: str | None = None
):
    def bar_update(ab: AliveBarPercentage, percent: int):
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
            listen_progress=lambda stdout: bar_update(bar, stdout.value),
            devel_su=devel_su
        ))
    if verbose:
        echo_stdout(OutResult(), verbose)


def ssh_common_remove_cli(
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
