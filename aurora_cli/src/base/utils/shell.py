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
from typing import Callable

from cffi.backend_ctypes import unicode

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError
from aurora_cli.src.base.utils.string import str_clear_line
from aurora_cli.src.base.utils.verbose import verbose_add_map, verbose_command_start


def shell_exec_command(
        args: [],
        listen: Callable[[str], None] | None = None,
        disable_sigint: bool = True,
) -> []:
    if not args:
        echo_stdout(OutResultError(TextError.shell_exec_command_empty()))
        exit(1)

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

    def set_out(out: str, is_error: bool | None = None):
        is_error = check_is_error(out) if is_error is None else is_error
        if is_error:
            stderr.append(out)
        else:
            stdout.append(out)

    command = verbose_command_start(args)

    try:
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=exec_fn) as process:
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
