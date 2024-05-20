import re
import string
from pathlib import Path, PosixPath
from typing import Callable

import paramiko
from paramiko.channel import ChannelFile
from paramiko.client import SSHClient

ssh_commands_verbose_save = []


def ssh_client_connect(
        ip: str,
        username: str,
        port: int,
        key: Path | str
) -> SSHClient | None:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if type(key) is PosixPath:
            client.connect(ip, username=username, key_filename=str(key), timeout=5, port=port)
        else:
            client.connect(ip, username=username, password=key, timeout=5, port=port)
        return client
    except (Exception,):
        return None


def ssh_exec_command(
        client: SSHClient,
        execute: str,
        listen_stdout: Callable[[str, int], None] = None,
        listen_stderr: Callable[[str, int], None] = None,
):
    global ssh_commands_verbose_save

    _, stdout, stderr = client.exec_command(execute, get_pty=True)

    def call_listen(out: [], listen: Callable[[str, int], None] = None):
        if listen:
            listen(out[-1], len(out) - 1)

    def read_lines(out: ChannelFile, listen: Callable[[str, int], None] = None):
        result = []
        try:
            for value in iter(out.readline, ""):
                value = str(value).strip()
                value = str(re.sub(r'[^' + string.printable + r'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\s]', '', value))
                value = str(re.sub(r'\s+', ' ', value))
                if value:
                    result.append(value)
                    call_listen(result, listen)
        except Exception as e:
            result.append('Exception: {}'.format(str(e)))
            call_listen(result, listen)
        return result

    _stdout = read_lines(stdout, listen_stdout)
    _stderr = read_lines(stderr, listen_stderr)

    ssh_commands_verbose_save.append({
        'command': execute,
        'stdout': _stdout,
        'stderr': _stderr,
    })

    return _stdout, _stderr


def ssh_verbose_map():
    global ssh_commands_verbose_save
    data = ssh_commands_verbose_save
    ssh_commands_verbose_save = []
    return data
