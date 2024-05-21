import re
from pathlib import Path, PosixPath
from typing import Callable

import click
import paramiko
from paramiko.channel import ChannelFile
from paramiko.client import SSHClient

from aurora_cli.src.base.helper import clear_str_line


def ssh_client_connect(
        host: str,
        username: str,
        port: int,
        auth: Path | str
) -> SSHClient | None:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if type(auth) is PosixPath:
            client.connect(host, username=username, key_filename=str(auth), timeout=5, port=port)
        else:
            client.connect(host, username=username, password=auth, timeout=5, port=port)
        return client
    except (Exception,):
        return None


def ssh_exec_command(
        client: SSHClient,
        execute: str,
        listen_stdout: Callable[[str, int], None] = None,
        listen_stderr: Callable[[str, int], None] = None,
):
    return _ssh_exec_command(client, execute, listen_stdout, listen_stderr)


@click.pass_context
def _ssh_exec_command(
        ctx: {},
        client: SSHClient,
        execute: str,
        listen_stdout: Callable[[str, int], None] = None,
        listen_stderr: Callable[[str, int], None] = None,
):
    _, stdout, stderr = client.exec_command(execute, get_pty=True)

    def call_listen(out: [], listen: Callable[[str, int], None] = None):
        if listen:
            listen(out[-1], len(out) - 1)

    def read_lines(out: ChannelFile, listen: Callable[[str, int], None] = None):
        result = []
        try:
            for value in iter(out.readline, ""):
                value = clear_str_line(str(value))
                if value:
                    result.append(value)
                    call_listen(result, listen)
        except Exception as e:
            result.append('Exception: {}'.format(str(e)))
            call_listen(result, listen)
        return result

    _stdout = read_lines(stdout, listen_stdout)
    _stderr = read_lines(stderr, listen_stderr)

    ctx.obj.add_verbose_map(
        command=execute,
        stdout=_stdout,
        stderr=_stderr,
    )

    return _stdout, _stderr
