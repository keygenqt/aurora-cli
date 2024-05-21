import subprocess

import click
from cffi.backend_ctypes import unicode

from aurora_cli.src.base.helper import clear_str_line


def shell_exec_command(args: []) -> []:
    return _shell_exec_command(args)


@click.pass_context
def _shell_exec_command(ctx: {}, args: []) -> []:
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
                value = clear_str_line(str(unicode(value.rstrip(), "utf-8")))
                if value:
                    set_out(value)
    except Exception as e:
        set_out(str(e), True)

    ctx.obj.add_verbose_map(
        command=' '.join(args),
        stdout=stdout,
        stderr=stderr,
    )

    return stdout, stderr
