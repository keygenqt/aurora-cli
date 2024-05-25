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

_commands_verbose_save = []


def verbose_add_map(command: str, stdout: [], stderr: []):
    _commands_verbose_save.append({
        'command': command,
        'stdout': stdout,
        'stderr': stderr,
    })


def verbose_seize_map():
    global _commands_verbose_save
    data = _commands_verbose_save
    _commands_verbose_save = []
    return data
