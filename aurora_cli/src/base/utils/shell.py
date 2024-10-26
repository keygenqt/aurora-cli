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
import shlex
import signal
import stat
import subprocess
from pathlib import Path
from typing import Any

from cffi.backend_ctypes import unicode

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult
from aurora_cli.src.base.utils.string import str_clear_line
from aurora_cli.src.base.utils.verbose import verbose_add_map, verbose_command_start


def shell_exec_command(
        args: [],
        cwd: Path = Path.cwd(),
        listen: Any = None,
        disable_sigint: bool = True,
        password = None
) -> []:
    if not args:
        echo_stdout(OutResultError(TextError.shell_exec_command_empty()))
        app_exit()

    stdout = []
    stderr = []

    # Ignore ctrl-c
    def exec_fn():
        if disable_sigint:
            signal.signal(signal.SIGINT, signal.SIG_IGN)

    def check_is_error(out: str) -> bool:
        if 'error' in out:
            return True
        return False

    def set_out(out: str, is_error: Any = None):
        is_error = check_is_error(out) if is_error is None else is_error
        if is_error:
            stderr.append(out)
        else:
            stdout.append(out)

    command = verbose_command_start(args)
    execute = ' '.join(args)
    if password:
        execute = ' '.join(['echo', password, '|', 'sudo', '-S'] + args)

    try:
        with subprocess.Popen(
                execute,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                preexec_fn=exec_fn,
                shell=True
        ) as process:
            for value in iter(lambda: process.stdout.readline(), ""):
                if not value:
                    break
                value = str_clear_line(str(unicode(value.rstrip(), "utf-8")))
                if listen:
                    listen(value)
                if value:
                    set_out(value)
    except Exception as e:
        set_out(str(e), True)

    if 'showvminfo' not in command:
        verbose_add_map(
            command=command,
            stdout=stdout,
            stderr=stderr,
        )

    return stdout, stderr


def shell_exec_app(path: Path) -> bool:
    os.chmod(str(path), os.stat(path).st_mode | stat.S_IEXEC)
    cmds = shlex.split(str(path))
    command = verbose_command_start(' '.join(cmds))
    try:
        subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        verbose_add_map(
            command=command,
            stdout=[],
            stderr=[],
        )
        return True
    except Exception as e:
        verbose_add_map(
            command=command,
            stdout=[],
            stderr=[str(e)],
        )
        return False


def shell_check_error_out(
        stdout: list,
        stderr: Any = None,
        search: Any = None
) -> OutResult:
    if stderr:
        return OutResultError(TextError.exec_command_error(), value=-1)
    else:
        if search:
            for line in stdout:
                for i, item in enumerate(search):
                    if item in line:
                        return OutResultError(TextError.exec_command_error(), value=i)
    return OutResult()
