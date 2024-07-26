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
from time import sleep
from typing import Any

from aurora_cli.src.base.common.features.image_features import image_crop_for_project
from aurora_cli.src.base.common.features.psdk_features import psdk_project_build
from aurora_cli.src.base.common.features.search_files import search_project_application_id
from aurora_cli.src.base.common.features.shell_features import shell_cpp_format
from aurora_cli.src.base.common.groups.device.device_package_features import (
    device_check_package_common,
    device_package_remove_common,
    device_package_install_common,
    device_package_run_common
)
from aurora_cli.src.base.common.groups.emulator.emulator_features import emulator_start_common
from aurora_cli.src.base.common.groups.emulator.emulator_package_features import (
    emulator_check_package_common,
    emulator_package_remove_common,
    emulator_package_install_common,
    emulator_package_run_common
)
from aurora_cli.src.base.common.groups.psdk.__tools import psdk_tool_check_is_project, psdk_tool_get_clang_format
from aurora_cli.src.base.common.groups.psdk.psdk_package_features import psdk_package_sign_common
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultError, OutResultInfo, echo_verbose
from aurora_cli.src.base.utils.tests import tests_exit


def psdk_project_format_common(
        project: Path,
        is_bar: bool = True
):
    tests_exit()
    psdk_tool_check_is_project(project)

    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        files = []
        files.extend(files_h)
        files.extend(files_cpp)
        result = shell_cpp_format(files, psdk_tool_get_clang_format(is_bar))
        if not result.is_error():
            echo_stdout(result)
        else:
            echo_stdout(result)
            app_exit()

    echo_stdout(OutResult(TextSuccess.project_format_success()))


def psdk_project_build_common(
        model_psdk: PsdkModel,
        model_device: Any,
        model_keys: Any,
        target: str,
        debug: bool,
        clean: bool,
        project: Path,
        is_apm: bool,
        is_install: bool,
        is_run: bool,
        verbose: bool,
        is_bar: bool = True
):
    tests_exit()
    psdk_tool_check_is_project(project)

    if is_install and is_apm and debug:
        echo_stdout(OutResultError(TextError.debug_apm_error()))
        app_exit()

    package = search_project_application_id(project)
    if not package:
        echo_stdout(OutResultError(TextError.search_application_id_error()))
        app_exit()

    bar = AliveBarPercentage()

    def out_check_result(out: OutResult):
        echo_stdout(out)
        if out.is_error():
            app_exit()

    def out_progress(percent: int, title: str):
        if is_bar:
            bar.update(percent, title, 12)
        else:
            echo_stdout(OutResultInfo(TextInfo.install_progress(), value=percent))

    result = psdk_project_build(
        tool=model_psdk.get_tool_path(),
        target=target,
        clean=clean,
        debug=debug,
        path=project,
        progress=lambda percent: out_progress(percent, 'build aurora')
    )

    out_check_result(result)
    rpms = result.value

    if (is_install or is_run) and model_device is None:
        emulator = EmulatorModel.get_model_user()
        if not emulator.is_on:
            emulator_start_common(emulator)
            sleep(5)

    if is_install:
        # sign rpm
        psdk_package_sign_common(model_psdk, model_keys, rpms)
        for rpm in rpms:
            # remove package if exit
            if is_apm:
                if model_device:
                    model = DeviceModel.get_model_by_host(model_device.host)
                    if device_check_package_common(model, package):
                        device_package_remove_common(
                            model=model,
                            package=package,
                            apm=is_apm,
                        )
                else:
                    model = EmulatorModel.get_model_root()
                    if emulator_check_package_common(model, package):
                        emulator_package_remove_common(
                            model=EmulatorModel.get_model_root(),
                            package=package,
                            apm=is_apm,
                        )
            # install package
            if model_device:
                device_package_install_common(
                    model=DeviceModel.get_model_by_host(model_device.host),
                    path=rpm,
                    apm=is_apm,
                )
            else:
                emulator_package_install_common(
                    model=EmulatorModel.get_model_root(),
                    path=rpm,
                    apm=is_apm,
                )

    if is_run:
        echo_verbose(verbose)
        sleep(2)
        if model_device:
            device_package_run_common(
                model=DeviceModel.get_model_by_host(model_device.host),
                package=package,
                run_mode='sandbox',
                path_project=str(project)
            )
        else:
            emulator_package_run_common(
                model=EmulatorModel.get_model_user(),
                package=package,
                run_mode='sandbox',
                path_project=str(project)
            )


def psdk_project_icons_common(
        project: Path,
        image: Path
):
    tests_exit()
    psdk_tool_check_is_project(project)
    path_icons = project / 'icons'
    result = image_crop_for_project(image, path_icons, search_project_application_id(project))
    echo_stdout(result)
