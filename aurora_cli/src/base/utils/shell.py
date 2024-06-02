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
import stat
import subprocess
from pathlib import Path

from cffi.backend_ctypes import unicode

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError
from aurora_cli.src.base.utils.string import str_clear_line
from aurora_cli.src.base.utils.verbose import verbose_add_map


def shell_exec_command(args: []) -> []:
    if not args:
        echo_stdout(OutResultError(TextError.shell_exec_command_empty()))
        exit(1)

    stdout = []
    stderr = []

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

    try:
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            for value in iter(lambda: process.stdout.readline(), ""):
                if not value:
                    break
                value = str_clear_line(str(unicode(value.rstrip(), "utf-8")))
                if value:
                    set_out(value)
    except Exception as e:
        set_out(str(e), True)

    verbose_add_map(
        command=' '.join(args),
        stdout=stdout,
        stderr=stderr,
    )

    return stdout, stderr


def shell_exec_app(path: Path) -> bool:
    os.chmod(str(path), os.stat(path).st_mode | stat.S_IEXEC)
    cmds = shlex.split(str(path))
    try:
        subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        verbose_add_map(
            command=' '.join(cmds),
            stdout=[],
            stderr=[],
        )
        return True
    except Exception as e:
        verbose_add_map(
            command=' '.join(cmds),
            stdout=[],
            stderr=[str(e)],
        )
        return False
