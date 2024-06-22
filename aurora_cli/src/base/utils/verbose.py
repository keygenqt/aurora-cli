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

from time import monotonic
from typing import Any

_commands_verbose_save = []
_start_time = {}


def verbose_command_start(command: Any) -> str:
    if isinstance(command, list):
        command = ' '.join(command)
    global _start_time
    _start_time[command] = monotonic()
    return command


def verbose_add_map(command: str, stdout: [], stderr: []):
    global _start_time
    out = {
        'command': command,
        'stdout': stdout,
        'stderr': stderr,
    }
    if command in _start_time:
        out['time'] = monotonic() - _start_time[command]
    _commands_verbose_save.append(out)


def verbose_seize_map():
    global _commands_verbose_save
    data = _commands_verbose_save
    _commands_verbose_save = []
    return data
