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
from pathlib import Path

from aurora_cli.src.base.constants.other import VM_MANAGE
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.convert import convert_video
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError, OutResultInfo
from aurora_cli.src.base.utils.path import path_gen_file_name
from aurora_cli.src.base.utils.shell import shell_exec_command


@check_dependency(DependencyApps.vboxmanage)
def vm_emulator_start() -> OutResult:
    result_vm_name = _vm_emulator_name()
    if result_vm_name.is_error():
        return result_vm_name

    result_vm_is_on = _vm_emulator_is_on(result_vm_name.value)
    if not result_vm_is_on.is_error():
        return OutResultInfo(TextInfo.emulator_start_locked())

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'startvm',
        result_vm_name.value
    ])
    if stderr:
        if 'already locked' in stderr[0]:
            return OutResultInfo(TextInfo.emulator_start_locked())
        else:
            return OutResultError(TextError.emulator_start_error())
    return OutResult(TextSuccess.emulator_start_success())


@check_dependency(DependencyApps.vboxmanage)
def vm_emulator_screenshot() -> OutResult:
    result_vm_name = _vm_emulator_name()
    if result_vm_name.is_error():
        return result_vm_name

    result_vm_is_on = _vm_emulator_is_on(result_vm_name.value)
    if result_vm_is_on.is_error():
        return result_vm_is_on

    screenshots = Path.home() / 'Pictures' / 'Screenshots'
    if not screenshots.is_dir():
        screenshots.mkdir(parents=True, exist_ok=True)

    screenshot = str(screenshots / path_gen_file_name('Screenshot_from_', 'png'))

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'controlvm',
        result_vm_name.value,
        'screenshotpng',
        screenshot
    ])
    if stdout or stderr:
        return OutResultError(TextError.emulator_screenshot_error())

    return OutResult(
        message=TextSuccess.emulator_screenshot_success(screenshot),
        value=screenshot
    )


@check_dependency(DependencyApps.vboxmanage, DependencyApps.ffmpeg)
def vm_emulator_record_start() -> OutResult:
    result_vm_name = _vm_emulator_name()
    if result_vm_name.is_error():
        return result_vm_name

    result_vm_is_on = _vm_emulator_is_on(result_vm_name.value)
    if result_vm_is_on.is_error():
        return result_vm_is_on

    result_vm_is_on_record = vm_emulator_is_on_record(result_vm_name.value)
    if not result_vm_is_on_record.is_error():
        return OutResultError(TextError.emulator_already_running_recording())

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'controlvm',
        result_vm_name.value,
        'recording',
        'on'
    ])
    if stdout or stderr:
        OutResultError(TextError.emulator_recording_video_start_error())
    return OutResult(TextSuccess.emulator_recording_video_start())


@check_dependency(DependencyApps.vboxmanage, DependencyApps.ffmpeg)
def vm_emulator_record_stop() -> OutResult:
    result_vm_name = _vm_emulator_name()
    if result_vm_name.is_error():
        return result_vm_name

    result_vm_is_on = _vm_emulator_is_on(result_vm_name.value)
    if result_vm_is_on.is_error():
        return result_vm_is_on

    result_vm_is_on_record = vm_emulator_is_on_record(result_vm_name.value)
    if result_vm_is_on_record.is_error():
        return result_vm_is_on_record

    result_vm_path = _vm_emulator_path(result_vm_name.value)
    if result_vm_path.is_error():
        return result_vm_path

    e_path = result_vm_path.value
    e_name = result_vm_name.value
    v_path = Path('{e_path}/{e_name}-screen0.webm'.format(e_path=e_path, e_name=e_name))
    s_path = Path.home() / 'Videos' / path_gen_file_name('Video_from_', 'mp4')

    if not v_path.is_file():
        return OutResultError(TextError.emulator_recording_video_file_not_found())

    if not s_path.parent.is_dir():
        s_path.parent.mkdir(parents=True, exist_ok=True)

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'controlvm',
        e_name,
        'recording',
        'off'
    ])
    if stdout or stderr:
        OutResultError(TextError.emulator_recording_video_stop_error())

    result = convert_video(v_path, s_path)
    if result.is_error():
        return result

    return OutResult(TextSuccess.emulator_recording_video_stop_with_save(str(s_path)))


@check_dependency(DependencyApps.vboxmanage)
def vm_emulator_is_on_record(emulator_name: str | None = None) -> OutResult:
    if not emulator_name:
        result_vm_name = _vm_emulator_name()
        if result_vm_name.is_error():
            return result_vm_name
        emulator_name = result_vm_name.value

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'showvminfo',
        emulator_name,
    ])
    for line in stdout:
        if 'Recording enabled:' in line and 'yes' in line:
            return OutResult()
    return OutResultError(TextError.emulator_not_running_recording())


@check_dependency(DependencyApps.vboxmanage)
def vm_emulator_ssh_key() -> OutResult:
    result_vm_name = _vm_emulator_name()
    if result_vm_name.is_error():
        return result_vm_name

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'showvminfo',
        result_vm_name.value,
    ])
    for line in stdout:
        if 'Snapshot folder:' in line:
            return OutResult(
                value=Path(os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(line.replace('Snapshot folder:', '').strip())
                        )
                    )
                )) / 'vmshare' / 'ssh' / 'private_keys' / 'sdk'
            )
    return OutResultError()


@check_dependency(DependencyApps.vboxmanage)
def _vm_emulator_name() -> OutResult:
    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'list',
        'vms',
    ])
    if stderr:
        return OutResultError(TextError.emulator_not_found())
    for line in stdout:
        if 'AuroraOS' in line:
            return OutResult(value=line.split('"')[1])
    return OutResultError(TextError.emulator_not_found())


@check_dependency(DependencyApps.vboxmanage)
def _vm_emulator_is_on(emulator_name: str) -> OutResult:
    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'list',
        'runningvms',
    ])
    for line in stdout:
        if emulator_name in line:
            return OutResult()
    return OutResultError(TextError.emulator_not_found_running())


@check_dependency(DependencyApps.vboxmanage)
def _vm_emulator_path(emulator_name: str) -> OutResult:
    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'showvminfo',
        emulator_name,
    ])
    for line in stdout:
        if 'Snapshot folder:' in line:
            return OutResult(
                value=os.path.dirname(line.replace('Snapshot folder:', '').strip())
            )
    return OutResultError(TextError.emulator_path_not_found())
