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
import os
import socket
from pathlib import PosixPath, Path

import paramiko
from paramiko.client import SSHClient

from aurora_cli.src.support.alive_bar.progress_alive_bar import ProgressAliveBar
from aurora_cli.src.support.helper import check_string_regex
from aurora_cli.src.support.output import echo_stdout, echo_stderr, VerboseType
from aurora_cli.src.support.texts import AppTexts


# Get ssh client
def get_ssh_client(
        ip: str,
        username: str,
        port: int,
        key: Path | str
) -> SSHClient | None:
    try:
        # Connect
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if type(key) is PosixPath:
            client.connect(ip, username=username, key_filename=str(key), timeout=5, port=port)
        else:
            client.connect(ip, username=username, password=key, timeout=5, port=port)
        return client
    except paramiko.ssh_exception.SSHException:
        pass
    except paramiko.ssh_exception.NoValidConnectionsError:
        pass
    except socket.gaierror:
        pass
    except TimeoutError:
        pass
    return None


def ssh_client_exec_command(
        client: SSHClient,
        execute: str,
        verbose: VerboseType,
        error_regx=None
):
    # Exec
    _, ssh_stdout, ssh_stderr = client.exec_command(execute, get_pty=True)

    is_error = False

    # Output
    for line in iter(ssh_stdout.readline, ""):
        line = str(line).strip()
        if error_regx and not is_error and error_regx:
            is_error = check_string_regex(line, error_regx)
        if verbose == VerboseType.verbose:
            echo_stdout(line)

    stderr = []

    for line in iter(ssh_stderr.readline, ""):
        line = str(line).strip()
        if error_regx and not is_error and error_regx:
            is_error = check_string_regex(line, error_regx)
        if 'Password' not in line:
            stderr.append(line.strip())

    # Output result
    if verbose and stderr:
        echo_stderr(str(stderr))

    if '|' in execute:
        execute = execute.split('|')[1].strip()

    if verbose == VerboseType.command:
        if stderr or is_error:
            echo_stderr(AppTexts.command_execute_error(execute))
        else:
            echo_stdout(AppTexts.command_execute_success(execute))

    if verbose == VerboseType.short:
        if is_error:
            echo_stderr(AppTexts.command_execute_error_short())
        else:
            echo_stdout(AppTexts.command_execute_success_short())


# Upload file
def upload_file_sftp(client: SSHClient, upload_path: str, file_path: str):
    if not client:
        return None
    try:
        # Create ssh bar
        bar = ProgressAliveBar(AppTexts.upload_success())
        # Get file name
        file_name = os.path.basename(file_path)
        # Upload file
        client.open_sftp().put(file_path, '{upload_path}/{file_name}'.format(
            upload_path=upload_path,
            file_name=file_name
        ), callback=bar.update)
    except paramiko.ssh_exception.SSHException:
        return False
    except FileNotFoundError:
        return False
    return True


# Upload file
def download_file_sftp(
        client: SSHClient,
        download_path: str,
        file_path: str,
        show_bar: bool = False
) -> str | None:
    if not client:
        return None
    try:
        # Get file name
        file_name = os.path.basename(download_path)
        # Path to file
        file_path = '{file_path}/{file_name}'.format(
            file_path=file_path,
            file_name=file_name
        )
        # Create ssh bar
        bar = ProgressAliveBar(AppTexts.download_success())
        # Upload file
        client.open_sftp().get(download_path, file_path, callback=bar.update if show_bar else None)
    except paramiko.ssh_exception.SSHException:
        return None
    except FileNotFoundError:
        return None
    return file_path
