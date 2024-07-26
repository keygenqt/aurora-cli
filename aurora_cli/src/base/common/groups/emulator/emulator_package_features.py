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

from aurora_cli.src.base.common.groups.common.ssh_commands import (
    ssh_run_common,
    ssh_install_common,
    ssh_remove_common,
    ssh_check_package
)
from aurora_cli.src.base.common.groups.emulator.__tools import emulator_tool_check_is_not_run
from aurora_cli.src.base.models.emulator_model import EmulatorModel


def emulator_package_run_common(
        model: EmulatorModel,
        package: str,
        run_mode: str,  # dart/gdb/sandbox
        path_project: str
):
    emulator_tool_check_is_not_run(model)
    ssh_run_common(model, package, run_mode, path_project)


def emulator_package_install_common(
        model: EmulatorModel,
        path: str,
        apm: bool,
):
    emulator_tool_check_is_not_run(model)
    ssh_install_common(model, path, apm)


def emulator_package_remove_common(
        model: EmulatorModel,
        package: str,
        apm: bool,
):
    emulator_tool_check_is_not_run(model)
    ssh_remove_common(model, package, apm)


def emulator_check_package_common(
        model: EmulatorModel,
        package: str,
) -> bool:
    if not model.is_on:
        return False
    return ssh_check_package(model, package)
