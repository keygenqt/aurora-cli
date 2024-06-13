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

from aurora_cli.src.base.common.features.flutter_features import (
    flutter_clear,
    flutter_get_pub,
    flutter_run_build_runner,
    flutter_build
)
from aurora_cli.src.base.common.features.image_features import image_crop_for_project
from aurora_cli.src.base.common.features.search_installed import search_project_application_id, \
    search_flutter_project_pubspec_key
from aurora_cli.src.base.common.features.shell_features import shell_dart_format, shell_cpp_format
from aurora_cli.src.base.common.groups.device.device_package_features import (
    device_package_install_common,
    device_package_remove_common,
    device_package_run_common,
    device_check_package_common
)
from aurora_cli.src.base.common.groups.emulator.emulator_features import emulator_start_common
from aurora_cli.src.base.common.groups.emulator.emulator_package_features import (
    emulator_package_install_common,
    emulator_package_remove_common,
    emulator_package_run_common,
    emulator_check_package_common
)
from aurora_cli.src.base.common.groups.flutter.__tools import (
    flutter_tool_get_clang_format,
    flutter_tool_check_is_project
)
from aurora_cli.src.base.common.groups.psdk.psdk_package_features import psdk_package_sign_common
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.models.flutter_model import FlutterModel
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultInfo, echo_stdout_verbose, OutResultError


def flutter_project_format_common(
        model: FlutterModel,
        project: Path,
        verbose: bool,
        is_bar: bool = True
):
    flutter_tool_check_is_project(project)

    files_dart = project.rglob('*.dart')
    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        files = []
        files.extend(files_h)
        files.extend(files_cpp)
        result = shell_cpp_format(files, flutter_tool_get_clang_format(verbose, is_bar))
        if not result.is_error():
            echo_stdout(result)
        else:
            echo_stdout(result, verbose)
            exit(1)

    # if dart files exist run dart format
    if files_dart:
        result = shell_dart_format(model.get_tool_dart(), str(project))
        if not result.is_error():
            echo_stdout(result)
        else:
            echo_stdout(result, verbose)
            exit(1)

    echo_stdout(OutResult(TextSuccess.project_format_success()), verbose)


def flutter_project_build_common(
        model_flutter: FlutterModel,
        model_psdk: PsdkModel,
        model_device: DeviceModel | None,
        model_keys: SignModel | None,
        target: str,
        mode: str,
        project: Path,
        is_apm: bool,
        is_install: bool,
        is_run: bool,
        verbose: bool,
        is_bar: bool = True
):
    flutter_tool_check_is_project(project)

    package = search_project_application_id(project)
    if not package:
        echo_stdout(OutResultError(TextError.search_application_id_error()))
        exit(1)

    bar = AliveBarPercentage()

    def out_check_result(out: OutResult):
        if out.is_error():
            echo_stdout(out, verbose)
            exit(1)
        else:
            echo_stdout(out)

    def out_progress(percent: int, title: str):
        if is_bar:
            bar.update(percent, title, 12)
        else:
            echo_stdout(OutResultInfo(TextInfo.install_progress(), value=percent))

    out_check_result(flutter_clear(
        flutter=model_flutter.get_tool_flutter(),
        path=project,
        progress=lambda percent: out_progress(percent, 'clean')
    ))

    out_check_result(flutter_get_pub(
        flutter=model_flutter.get_tool_flutter(),
        path=project,
        progress=lambda percent: out_progress(percent, 'pub get')
    ))

    if search_flutter_project_pubspec_key(project, 'build_runner'):
        out_check_result(flutter_run_build_runner(
            flutter=model_flutter.get_tool_flutter(),
            path=project,
            progress=lambda percent: out_progress(percent, 'build_runner')
        ))

    result = flutter_build(
        psdk_dir=model_psdk.get_psdk_dir(),
        target=target,
        flutter=model_flutter.get_tool_flutter(),
        mode=mode,
        path=project,
        progress=lambda percent: out_progress(percent, 'build aurora')
    )

    out_check_result(result)
    rpms = result.value

    if (is_install or is_run) and model_device is None:
        emulator = EmulatorModel.get_model_user(verbose)
        if not emulator.is_on:
            emulator_start_common(emulator, verbose)
            sleep(1)

    if is_install:
        for rpm in rpms:
            # sign rpm
            psdk_package_sign_common(model_psdk, model_keys, rpm, verbose)
            sleep(1)
            # remove package if exit
            if model_device:
                model = DeviceModel.get_model_by_host(model_device.host, verbose)
                if device_check_package_common(model, package, verbose):
                    device_package_remove_common(
                        model=model,
                        package=package,
                        apm=is_apm,
                        verbose=verbose
                    )
            else:
                model = EmulatorModel.get_model_root(verbose)
                if emulator_check_package_common(model, package, verbose):
                    emulator_package_remove_common(
                        model=EmulatorModel.get_model_root(verbose),
                        package=package,
                        apm=is_apm,
                        verbose=verbose
                    )
            # install package
            if model_device:
                device_package_install_common(
                    model=DeviceModel.get_model_by_host(model_device.host, verbose),
                    path=rpm,
                    apm=is_apm,
                    verbose=verbose
                )
            else:
                emulator_package_install_common(
                    model=EmulatorModel.get_model_root(verbose),
                    path=rpm,
                    apm=is_apm,
                    verbose=verbose
                )

    if is_run:
        sleep(1)
        if model_device:
            device_package_run_common(
                model=DeviceModel.get_model_by_host(model_device.host, verbose),
                package=package,
                verbose=verbose
            )
        else:
            emulator_package_run_common(
                model=EmulatorModel.get_model_user(verbose),
                package=package,
                verbose=verbose
            )
    else:
        echo_stdout_verbose(verbose)


def flutter_project_debug_common(
        model: FlutterModel,
        project: Path,
        verbose: bool
):
    flutter_tool_check_is_project(project)

    # @todo
    print('Coming soon')


def flutter_project_report_common(project: Path, verbose: bool):
    flutter_tool_check_is_project(project)

    # @todo
    print('Coming soon')

    echo_stdout(OutResult(TextSuccess.flutter_project_report_success()), verbose)


def flutter_project_icons_common(project: Path, image: Path, verbose: bool):
    flutter_tool_check_is_project(project)
    path_icons = project / 'aurora' / 'icons'
    result = image_crop_for_project(image, path_icons)
    echo_stdout(result, verbose)
