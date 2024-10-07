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
import atexit
import io
import os
import signal
import sys
import traceback
from typing import Callable, Any

import click

from aurora_cli.src.base.utils.argv import argv_is_verbose, argv_is_test, argv_is_help, argv_is_api
from aurora_cli.src.base.utils.cache_settings import cache_settings_get, CacheSettingsKey
from aurora_cli.src.base.utils.exceptions import AppExit


def app_crash_out(e: Exception):
    print(click.style('An unexpected error occurred in the application.', fg='red'))
    if argv_is_verbose():
        traceback.print_exception(e)


def app_abort_handler(callback: Callable[[], None]):
    def signal_handler(s, f):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        callback()

    signal.signal(signal.SIGINT, signal_handler)


def app_crash_handler(callback: Callable[[Any], None]):
    def exception_handler(exception_type, exception, _):
        if exception_type is AppExit:
            callback(None)
        else:
            callback(exception)

    sys.excepthook = exception_handler


def app_help_handler(callback: Callable[[str], None]):
    _stdout = None
    _stderr = None

    if argv_is_help():
        _stdout = sys.stdout
        sys.stdout = _io_stdout = io.StringIO()

    _stderr = sys.stderr
    sys.stderr = _io_stderr = io.StringIO()

    def exit_handler():
        out = None
        err = None
        if _stdout:
            sys.stdout = _stdout
            out = '\n'.join(_io_stdout.getvalue().splitlines())
        if _stderr:
            sys.stderr = _stderr
            err = '\n'.join(_io_stderr.getvalue().splitlines())
        if out:
            callback(out)
        if err:
            callback(err)

    atexit.register(exit_handler)


def app_language() -> str:
    settings_val = cache_settings_get(CacheSettingsKey.language)
    if settings_val:
        return settings_val

    if 'ru_RU' in os.getenv("LANG"):
        return 'ru'
    else:
        return 'en'


def app_exit(code: int = 1):
    if argv_is_test() or argv_is_api():
        exit(code)
    else:
        raise AppExit(code)
