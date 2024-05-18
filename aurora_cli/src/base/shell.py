import subprocess
from typing import Callable

from cffi.backend_ctypes import unicode

commands_verbose_save = []


def shell_command(
        args: [],
        listen: Callable[[str, int, bool], None] = None,
) -> []:
    global commands_verbose_save

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
        if listen:
            listen(out, len(stderr) + len(stdout), is_error)

    try:
        with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            for line in iter(lambda: process.stdout.readline(), ""):
                if not line:
                    break
                line = unicode(line.rstrip(), "utf-8").strip()
                if line:
                    set_out(line)
    except Exception as e:
        set_out(str(e), True)

    commands_verbose_save.append({
        'command': ' '.join(args),
        'stdout': stdout,
        'stderr': stderr,
    })

    return stdout, stderr


def shell_verbose_map():
    global commands_verbose_save
    data = commands_verbose_save
    commands_verbose_save = []
    return data
