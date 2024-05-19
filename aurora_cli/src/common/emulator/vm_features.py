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

from aurora_cli.src.base.common.texts.error import TextError
from aurora_cli.src.base.common.texts.info import TextInfo
from aurora_cli.src.base.common.texts.success import TextSuccess
from aurora_cli.src.base.helper import gen_file_name
from aurora_cli.src.base.output import OutResult, OutResult418, OutResult500
from aurora_cli.src.base.shell import shell_command

VM_MANAGE = "VBoxManage"


def vm_emulator_name() -> OutResult:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'list',
        'vms',
    ])
    if stderr:
        return OutResult()
    for line in stdout:
        if 'AuroraOS' in line:
            return OutResult(value=line.split('"')[1])
    return OutResult()


def vm_emulator_path() -> OutResult:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'showvminfo',
        vm_emulator_name().value,
    ])
    for line in stdout:
        if 'Snapshot folder:' in line:
            return OutResult(
                value=os.path.dirname(line.replace('Snapshot folder:', '').strip())
            )
    return OutResult500()


def vm_emulator_ssh_key() -> OutResult:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'showvminfo',
        vm_emulator_name().value,
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
    return OutResult500()


def vm_emulator_start() -> OutResult:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'startvm',
        vm_emulator_name().value
    ])
    if stderr:
        if 'already locked' in stderr[0]:
            return OutResult418(TextInfo.emulator_start_locked())
        else:
            return OutResult500(TextError.emulator_start_error())
    return OutResult(TextSuccess.emulator_start_success())


def vm_emulator_screenshot() -> OutResult:
    screenshots = Path.home() / 'Pictures' / 'Screenshots'
    if not screenshots.is_dir():
        screenshots.mkdir(parents=True, exist_ok=True)

    screenshot = str(screenshots / gen_file_name('Screenshot_from_', 'png'))

    stdout, stderr = shell_command([
        VM_MANAGE,
        'controlvm',
        vm_emulator_name().value,
        'screenshotpng',
        screenshot
    ])
    if stdout or stderr:
        return OutResult500(TextError.emulator_screenshot_error())

    return OutResult(
        message=TextSuccess.emulator_screenshot_success(screenshot),
        value=screenshot
    )


def vm_emulator_record_start() -> OutResult:
    if vm_emulator_record_is_on().value:
        return OutResult418(TextInfo.emulator_recording_video_start_already())
    stdout, stderr = shell_command([
        VM_MANAGE,
        'controlvm',
        vm_emulator_name().value,
        'recording',
        'on'
    ])
    if stdout or stderr:
        OutResult500(TextError.emulator_recording_video_start_error())
    return OutResult(TextSuccess.emulator_recording_video_start())


def vm_emulator_record_stop() -> OutResult:
    if not vm_emulator_record_is_on().value:
        return OutResult418(TextInfo.emulator_recording_video_stop_already())

    e_path = vm_emulator_path().value
    e_name = vm_emulator_name().value
    v_path = Path('{e_path}/{e_name}-screen0.webm'.format(e_path=e_path, e_name=e_name))
    s_path = Path.home() / 'Videos' / gen_file_name('Video_from_', 'mp4')

    if not v_path.is_file():
        return OutResult500(TextError.emulator_recording_video_file_not_found())

    if not s_path.parent.is_dir():
        s_path.parent.mkdir(parents=True, exist_ok=True)

    result = vm_emulator_record_video_convert(v_path, s_path)
    if result.is_error():
        return result

    stdout, stderr = shell_command([
        VM_MANAGE,
        'controlvm',
        vm_emulator_name().value,
        'recording',
        'off'
    ])
    if stdout or stderr:
        OutResult500(TextError.emulator_recording_video_stop_error())
    return OutResult(TextSuccess.emulator_recording_video_stop())


def vm_emulator_record_is_on() -> OutResult:
    stdout, stderr = shell_command([
        VM_MANAGE,
        'showvminfo',
        vm_emulator_name().value,
    ])
    for line in stdout:
        if 'Recording enabled:' in line and 'yes' in line:
            return OutResult(value=True)
    return OutResult(value=False)


def vm_emulator_record_video_convert(v_path: Path, s_path: Path) -> OutResult:
    stdout, stderr = shell_command([
        'ffmpeg',
        '-i',
        str(v_path),
        '-c:v',
        'libx264',
        '-preset',
        'slow',
        '-crf',
        '22',
        '-c:a',
        'copy',
        '-b:a',
        '128k',
        str(s_path),
    ])
    if stderr:
        return OutResult500(TextError.emulator_recording_video_convert_error())
    return OutResult(
        message=TextSuccess.emulator_recording_video_convert(str(s_path)),
        value=str(s_path)
    )
