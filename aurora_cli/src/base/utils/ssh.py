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
from typing import Callable, Any

import paramiko
from paramiko.channel import ChannelFile
from paramiko.client import SSHClient

from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.string import str_clear_line
from aurora_cli.src.base.utils.verbose import verbose_add_map, verbose_command_start


@check_dependency(DependencyApps.ssh)
def ssh_client_connect(
        host: str,
        username: str,
        port: int,
        auth: Any
) -> Any:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if type(auth) is PosixPath:
            client.connect(host, username=username, key_filename=str(auth), timeout=2, port=port)
        else:
            client.connect(host, username=username, password=auth, timeout=2, port=port)
        return client
    except (Exception,):
        return None


@check_dependency(DependencyApps.ssh)
def ssh_exec_command(
        client: SSHClient,
        execute: str,
        listen_stdout: Callable[[str, int], None] = None,
        listen_stderr: Callable[[str, int], None] = None,
):
    command = verbose_command_start(execute)
    _, stdout, stderr = client.exec_command(execute, get_pty=True)

    def call_listen(out: [], listen: Callable[[str, int], None] = None):
        if listen:
            listen(out[-1], len(out) - 1)

    def read_lines(out: ChannelFile, listen: Callable[[str, int], None] = None):
        result = []
        try:
            for value in iter(out.readline, ""):
                value = str_clear_line(str(value))
                if value:
                    result.append(value)
                    call_listen(result, listen)
        except Exception as e:
            result.append('Exception: {}'.format(str(e)))
            call_listen(result, listen)
        return result

    stdout = read_lines(stdout, listen_stdout)
    stderr = read_lines(stderr, listen_stderr)

    verbose_add_map(
        command=command,
        stdout=stdout,
        stderr=stderr,
    )

    return stdout, stderr
