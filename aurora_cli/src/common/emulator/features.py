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
from pathlib import Path

from aurora_cli.src.base.common.texts.error import TextError
from aurora_cli.src.base.common.texts.info import TextInfo
from aurora_cli.src.base.common.texts.success import TextSuccess
from aurora_cli.src.base.helper import gen_file_name
from aurora_cli.src.base.output import Out, Out418, Out500
from aurora_cli.src.base.shell import shell_command

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


def emulator_start() -> Out:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'startvm',
        _emulator_name()
    ])
    if stderr:
        if 'already locked' in stderr[0]:
            return Out418(TextInfo.emulator_start_locked())
        else:
            return Out500(TextError.emulator_start_error())
    return Out(TextSuccess.emulator_start_success())


def emulator_screenshot() -> Out:
    screenshots = Path.home() / 'Pictures' / 'Screenshots'
    if not screenshots.is_dir():
        screenshots.mkdir(parents=True, exist_ok=True)

    screenshot = str(screenshots / gen_file_name('Screenshot_from_', 'png'))

    stdout, stderr = shell_command([
        VM_MANAGE,
        'controlvm',
        _emulator_name(),
        'screenshotpng',
        screenshot
    ])
    if stdout or stderr:
        return Out500(TextError.emulator_screenshot_error())

    return Out(TextSuccess.emulator_screenshot_success(screenshot), data=screenshot)
