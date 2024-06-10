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

from aurora_cli.src.base.common.groups.impl.ssh_commands import (
    ssh_command_common,
    ssh_run_common,
    ssh_upload_common,
    ssh_install_common,
    ssh_remove_common
)
from aurora_cli.src.base.constants.other import VM_MANAGE
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.convert import convert_video
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError, OutResultInfo, echo_stdout
from aurora_cli.src.base.utils.path import path_gen_file_name
from aurora_cli.src.base.utils.shell import shell_exec_command


def _check_is_not_run(model: EmulatorModel, verbose: bool):
    if not model.is_on:
        echo_stdout(OutResultError(TextError.emulator_not_found_running()), verbose)
        exit(1)


@check_dependency(DependencyApps.vboxmanage)
def emulator_start_common(model: EmulatorModel, verbose: bool):
    if model.is_on:
        echo_stdout(OutResultInfo(TextInfo.emulator_start_locked()), verbose)
        exit(1)

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'startvm',
        model.name
    ])
    if stderr:
        if 'already locked' in stderr[0]:
            echo_stdout(OutResultInfo(TextInfo.emulator_start_locked()), verbose)
            exit(1)
        else:
            echo_stdout(OutResultError(TextError.emulator_start_error()), verbose)
            exit(1)
    echo_stdout(OutResult(TextSuccess.emulator_start_success()), verbose)


@check_dependency(DependencyApps.vboxmanage)
def emulator_screenshot_common(model: EmulatorModel, verbose: bool):
    _check_is_not_run(model, verbose)

    screenshots = Path.home() / 'Pictures' / 'Screenshots'
    if not screenshots.is_dir():
        screenshots.mkdir(parents=True, exist_ok=True)

    screenshot = str(screenshots / path_gen_file_name('Screenshot_from_', 'png'))

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'controlvm',
        model.name,
        'screenshotpng',
        screenshot
    ])
    if stdout or stderr:
        echo_stdout(OutResultError(TextError.emulator_screenshot_error()), verbose)
        exit(1)

    echo_stdout(OutResult(
        message=TextSuccess.emulator_screenshot_success(screenshot),
        value=screenshot
    ), verbose)


@check_dependency(DependencyApps.vboxmanage, DependencyApps.ffmpeg)
def emulator_recording_start_common(model: EmulatorModel, verbose: bool):
    _check_is_not_run(model, verbose)
    if model.is_record:
        echo_stdout(OutResultError(TextError.emulator_already_running_recording()), verbose)
        exit(1)

    stdout, stderr = shell_exec_command([
        VM_MANAGE,
        'controlvm',
        model.name,
        'recording',
        'on'
    ])
    if stdout or stderr:
        echo_stdout(OutResultError(TextError.emulator_recording_video_start_error()), verbose)
        exit(1)
    echo_stdout(OutResult(TextSuccess.emulator_recording_video_start()), verbose)


@check_dependency(DependencyApps.vboxmanage, DependencyApps.ffmpeg)
def emulator_recording_stop_common(model: EmulatorModel, verbose: bool):
    _check_is_not_run(model, verbose)
    if not model.is_record:
        echo_stdout(OutResultError(TextError.emulator_not_running_recording()), verbose)
        exit(1)

    e_path = model.path
    e_name = model.name
    v_path = Path('{e_path}/{e_name}-screen0.webm'.format(e_path=e_path, e_name=e_name))
    s_path = Path.home() / 'Videos' / path_gen_file_name('Video_from_', 'mp4')

    if not v_path.is_file():
        echo_stdout(OutResultError(TextError.emulator_recording_video_file_not_found()), verbose)
        exit(1)

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
        echo_stdout(result, verbose)
        exit(1)

    echo_stdout(OutResult(TextSuccess.emulator_recording_video_stop_with_save(str(s_path))), verbose)


def emulator_command_common(
        model: EmulatorModel,
        execute: str,
        verbose: bool
):
    _check_is_not_run(model, verbose)
    ssh_command_common(model, execute, verbose)


def emulator_upload_common(
        model: EmulatorModel,
        path: str,
        verbose: bool
):
    _check_is_not_run(model, verbose)
    ssh_upload_common(model, path, verbose)


def emulator_package_run_common(
        model: EmulatorModel,
        package: str,
        verbose: bool
):
    _check_is_not_run(model, verbose)
    ssh_run_common(model, package, verbose)


def emulator_package_install_common(
        model: EmulatorModel,
        path: str,
        apm: bool,
        verbose: bool
):
    _check_is_not_run(model, verbose)
    ssh_install_common(model, path, apm, verbose)


def emulator_package_remove_common(
        model: EmulatorModel,
        package: str,
        apm: bool,
        verbose: bool
):
    _check_is_not_run(model, verbose)
    ssh_remove_common(model, package, apm, verbose)
