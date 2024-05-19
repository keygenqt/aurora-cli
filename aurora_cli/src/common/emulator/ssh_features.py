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
from pathlib import Path, PosixPath

import paramiko
from paramiko.channel import ChannelFile
from paramiko.client import SSHClient

from aurora_cli.src.base.common.texts.error import TextError
from aurora_cli.src.base.common.texts.success import TextSuccess
from aurora_cli.src.base.output import OutResult, OutResult500
from aurora_cli.src.common.emulator.vm_features import vm_emulator_ssh_key


def _ssh_client_exec_command(
        client: SSHClient,
        execute: str,
):
    _, stdout, stderr = client.exec_command(execute, get_pty=True)

    def read_lines(out: ChannelFile):
        result = []
        try:
            for value in iter(out.readline, ""):
                value = str(value).strip()
                result.append(value)
        except Exception as e:
            result.append('Exception: {}'.format(str(e)))
        return result

    return read_lines(stdout), read_lines(stderr)


# Get ssh client
def _get_ssh_client(
        ip: str,
        username: str,
        port: int,
        key: Path | str
) -> OutResult:
    try:
        # Connect
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if type(key) is PosixPath:
            client.connect(ip, username=username, key_filename=str(key), timeout=5, port=port)
        else:
            client.connect(ip, username=username, password=key, timeout=5, port=port)
        return OutResult(value=client)
    except (Exception,):
        if type(key) is PosixPath:
            return OutResult500(TextError.ssh_connect_emulator_error())
        else:
            return OutResult500(TextError.ssh_connect_device_error())


def get_ssh_client_emulator(user: str = 'defaultuser') -> OutResult:
    # Get path to key
    result = vm_emulator_ssh_key()
    if result.is_error():
        return result
    # Get ssh client
    return _get_ssh_client(
        'localhost',
        user,
        2223,
        result.value
    )


def get_ssh_client_device(ip: str, port: int, password: str) -> OutResult:
    return _get_ssh_client(
        ip,
        'defaultuser',
        port,
        password
    )


def ssh_command(
        client: SSHClient,
        execute: str
) -> OutResult:
    stdout, stderr = _ssh_client_exec_command(client, execute)
    return OutResult(
        message=TextSuccess.emulator_exec_command_success(
            execute=execute
        ),
        value={
            'stdout': stdout,
            'stderr': stderr,
        }
    )


def ssh_run(
        client: SSHClient,
        package: str
) -> OutResult:
    return OutResult()


def ssh_upload(
        client: SSHClient,
        path: []
) -> OutResult:
    return OutResult()


def ssh_install(
        client: SSHClient,
        path: [],
        apm: bool
) -> OutResult:
    return OutResult()


def ssh_remove(
        client: SSHClient,
        package: str,
        apm: bool
) -> OutResult:
    return OutResult()
