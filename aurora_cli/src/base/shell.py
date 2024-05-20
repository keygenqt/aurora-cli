import re
import string
import subprocess

from cffi.backend_ctypes import unicode

shell_commands_verbose_save = []


def shell_exec_command(args: []) -> []:
    global shell_commands_verbose_save

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
                value = unicode(value.rstrip(), "utf-8")
                value = str(value).strip()
                value = str(re.sub(r'[^' + string.printable + r'абвгдеёжзийклмнопрстуфхцчшщъыьэюя\s]', '', value))
                value = str(re.sub(r'\s+', ' ', value))
                if value:
                    set_out(value)
    except Exception as e:
        set_out(str(e), True)

    shell_commands_verbose_save.append({
        'command': ' '.join(args),
        'stdout': stdout,
        'stderr': stderr,
    })

    return stdout, stderr


def shell_verbose_map():
    global shell_commands_verbose_save
    data = shell_commands_verbose_save
    shell_commands_verbose_save = []
    return data
