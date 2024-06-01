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
from typing import Any

from aurora_cli.src.api.group_api import group_api
from aurora_cli.src.cli.group_build import group_build
from aurora_cli.src.cli.group_debug import group_debug
from aurora_cli.src.cli.group_device import group_device
from aurora_cli.src.cli.group_emulator import group_emulator
from aurora_cli.src.cli.group_flutter import group_flutter
from aurora_cli.src.cli.group_psdk import group_psdk
from aurora_cli.src.cli.group_sdk import group_sdk
from aurora_cli.src.cli.group_sundry import group_sundry


# noinspection PyTypeChecker
def click_init_groups(fun: Any):
    fun.add_command(group_api)
    fun.add_command(group_build)
    fun.add_command(group_debug)
    fun.add_command(group_device)
    fun.add_command(group_emulator)
    fun.add_command(group_flutter)
    fun.add_command(group_psdk)
    fun.add_command(group_sdk)
    fun.add_command(group_sundry)
