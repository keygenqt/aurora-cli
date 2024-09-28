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

import json
import re
from pathlib import Path
from time import sleep
from typing import Any

from aurora_cli.src.base.common.features.flutter_features import (
    flutter_project_clear,
    flutter_project_get_pub,
    flutter_project_run_build_runner,
    flutter_project_build
)
from aurora_cli.src.base.common.features.image_features import image_crop_for_project
from aurora_cli.src.base.common.features.request_version import request_flutter_plugins
from aurora_cli.src.base.common.features.search_files import (
    search_project_application_id,
    search_flutter_project_pubspec_key
)
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
from aurora_cli.src.base.out.flutter_report_plugins import gen_flutter_report_plugins
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout, OutResult, OutResultInfo, OutResultError, echo_verbose
from aurora_cli.src.base.utils.tests import tests_exit


def flutter_project_format_common(
        model: FlutterModel,
        project: Path,
        is_bar: bool = True
):
    tests_exit()

    flutter_tool_check_is_project(project)

    files_dart = project.rglob('*.dart')
    files_h = project.rglob('*.h')
    files_cpp = project.rglob('*.cpp')

    # if C++ files exist run clang-format format
    if files_h or files_cpp:
        files = []
        files.extend(files_h)
        files.extend(files_cpp)
        result = shell_cpp_format(files, flutter_tool_get_clang_format(is_bar))
        echo_stdout(result)
        if result.is_error():
            app_exit()

    # if dart files exist run dart format
    if files_dart:
        result = shell_dart_format(model.get_tool_dart(), str(project))
        echo_stdout(result)
        if result.is_error():
            app_exit()

    echo_stdout(OutResult(TextSuccess.project_format_success()))


def flutter_project_build_common(
        model_flutter: FlutterModel,
        model_psdk: PsdkModel,
        model_device: Any,
        model_keys: Any,
        target: str,
        debug: bool,
        clean: bool,
        pub_get: bool,
        build_runner: bool,
        run_mode: Any,  # dart/gdb/sandbox/None
        project: Path,
        is_apm: bool,
        is_install: bool,
        verbose: bool,
        is_bar: bool = True
):
    tests_exit()
    flutter_tool_check_is_project(project)

    if (project / 'example').is_dir():
        project = project / 'example'

    if is_apm and run_mode == 'gdb':
        echo_stdout(OutResultError(TextError.debug_apm_gdb_error()))
        app_exit()

    package = search_project_application_id(project)
    if not package:
        echo_stdout(OutResultError(TextError.search_application_id_error()))
        app_exit()

    bar = AliveBarPercentage()
    is_fist = not (project / '.dart_tool').is_dir() or clean

    def out_check_result(out: OutResult):
        echo_stdout(out)
        if out.is_error():
            app_exit()

    def out_progress(percent: int, title: str):
        if is_bar:
            bar.update(percent, title, 12)
        else:
            echo_stdout(OutResultInfo(TextInfo.install_progress(), value=percent))

    if clean:
        (project / '.dart_tool').unlink(missing_ok=True)
        out_check_result(flutter_project_clear(
            flutter=model_flutter.get_tool_flutter(),
            path=project,
            progress=lambda percent: out_progress(percent, 'clean')
        ))

    if is_fist or pub_get:
        out_check_result(flutter_project_get_pub(
            flutter=model_flutter.get_tool_flutter(),
            path=project,
            progress=lambda percent: out_progress(percent, 'pub get')
        ))

    if search_flutter_project_pubspec_key(project, 'build_runner') and is_fist or build_runner:
        out_check_result(flutter_project_run_build_runner(
            flutter=model_flutter.get_tool_flutter(),
            path=project,
            progress=lambda percent: out_progress(percent, 'build_runner')
        ))

    result = flutter_project_build(
        psdk_dir=model_psdk.get_psdk_dir(),
        target=target,
        flutter=model_flutter.get_tool_flutter(),
        debug=debug,
        path=project,
        progress=lambda percent: out_progress(percent, 'build aurora')
    )

    out_check_result(result)
    rpms = result.value

    if (is_install or run_mode) and model_device is None:
        if 'x86_64' not in target:
            echo_stdout(OutResultError(TextError.run_emulator_arch_error()))
            app_exit()
        emulator = EmulatorModel.get_model_user()
        if not emulator.is_on:
            emulator_start_common(emulator)
            sleep(5)

    if is_install:
        # sign rpm
        psdk_package_sign_common(model_psdk, model_keys, rpms)
        if run_mode and is_apm:
            echo_stdout(OutResultInfo(TextInfo.install_debug_apm_dart_debug()))
            rpms = [rpms[-1]]

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

    if run_mode:
        echo_verbose(verbose)
        sleep(2)
        if model_device:
            device_package_run_common(
                model=DeviceModel.get_model_by_host(model_device.host),
                package=package,
                run_mode=run_mode,
                path_project=str(project)
            )
        else:
            emulator_package_run_common(
                model=EmulatorModel.get_model_user(),
                package=package,
                run_mode=run_mode,
                path_project=str(project)
            )


def flutter_project_report_common(
        model: FlutterModel,
        project: Path,
        is_bar: bool = True
):
    from weasyprint import HTML

    tests_exit()

    flutter_tool_check_is_project(project)

    bar = AliveBarPercentage()

    def out_check_result(out: OutResult):
        echo_stdout(out)
        if out.is_error():
            app_exit()

    def out_progress(percent: int):
        if is_bar:
            bar.update(percent)
        else:
            echo_stdout(OutResultInfo(TextInfo.install_progress(), value=percent))

    available = [
        'dbus',
        'build_runner',
        'build_runner_core',
        'flutter_cache_manager',
        'cached_network_image',
        'google_fonts',
    ]

    result = request_flutter_plugins()
    if result.is_error():
        available_impl = []
    else:
        available_impl = list(dict.fromkeys(
            [plugin.split('-')[0].replace('_aurora', '') for plugin in result.value if '_aurora' in plugin]))

    echo_stdout(OutResultInfo(TextInfo.flutter_project_pub_get()))

    out_check_result(flutter_project_get_pub(
        flutter=model.get_tool_flutter(),
        path=project,
        progress=lambda percent: out_progress(percent)
    ))

    package_config = project / '.dart_tool' / 'package_config.json'

    with open(package_config, 'r') as file:
        data = json.loads(file.read())

    if not data and not data['packages']:
        echo_stdout(OutResultError(TextError.flutter_read_json_error()))
        app_exit()

    find_plugins_nps = []
    find_plugins_ps = []

    keys = '|'.join([
        '_android',
        '_ios',
        '_linux',
        '_macos',
        '_web',
        '_windows',
        '_aurora'
    ])

    for item in data['packages']:
        plugin = Path(item['rootUri'].replace('file://', '')) / 'pubspec.yaml'
        if plugin.is_file():
            with open(plugin, 'r') as file:
                if item['name'][0] != '_':
                    if file.read().find("platforms:") == -1:
                        find_plugins_nps.append(item['name'])
                    else:
                        find_plugins_ps.append(item['name'])

    find_plugins_nps = list(dict.fromkeys(find_plugins_nps))
    find_plugins_ps = list(dict.fromkeys([re.sub(f'(.+)({keys})', r'\1', plugin) for plugin in find_plugins_ps]))
    find_plugins_aps = [plugin for plugin in find_plugins_ps if plugin in available or plugin in available_impl]

    line_name = search_flutter_project_pubspec_key(project, 'name')
    line_desc = search_flutter_project_pubspec_key(project, 'description')

    if not line_name:
        echo_stdout(OutResultError(TextError.flutter_read_yaml_error()))
        app_exit()
    else:
        line_name = line_name.replace('name: ', '')

    if line_desc:
        line_desc = line_desc.replace('description: ', '')

    echo_stdout(OutResultInfo(TextInfo.flutter_gen_plugins_report()))

    path_out = project / 'plugins_report.pdf'
    html_out = gen_flutter_report_plugins(
        name=line_name,
        description=line_desc,
        find_plugins_nps=find_plugins_nps,
        find_plugins_ps=find_plugins_ps,
        find_plugins_aps=find_plugins_aps,
    )

    HTML(string=html_out).write_pdf(path_out)

    echo_stdout(OutResult(TextSuccess.flutter_project_report_success(str(path_out)), value=path_out))


def flutter_project_icons_common(
        project: Path,
        image: Path
):
    if argv_is_test():
        echo_stdout(OutResult())
        app_exit(0)

    flutter_tool_check_is_project(project)

    if (project / 'example').is_dir():
        project = project / 'example'

    path_icons = project / 'aurora' / 'icons'
    result = image_crop_for_project(image, path_icons)
    echo_stdout(result)
