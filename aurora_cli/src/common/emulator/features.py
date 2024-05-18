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

from aurora_cli.src.base.shell import shell_command, ResultExec

VM_MANAGE = "VBoxManage"


def _emulator_name() -> str | None:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'list',
        'vms',
    ])
    if stderr:
        return None
    for line in stdout:
        if 'AuroraOS' in line:
            return line.split('"')[1]
    return None


def emulator_start() -> ResultExec:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'startvm',
        _emulator_name()
    ])
    if stderr:
        if 'already locked' in stderr[0]:
            return ResultExec.locked
        else:
            return ResultExec.error
    return ResultExec.success
