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
import traceback
from typing import Any

import click

from aurora_cli.src.api.group_api import group_api
from aurora_cli.src.base.utils.argv import argv_is_verbose
from aurora_cli.src.cli.group_device import group_device
from aurora_cli.src.cli.group_emulator import group_emulator


# noinspection PyTypeChecker
def app_init_groups(fun: Any):
    fun.add_command(group_api)
    fun.add_command(group_emulator)
    fun.add_command(group_device)


def app_crash_out(e: Exception):
    print(click.style('An unexpected error occurred in the application.', fg='red'))
    if argv_is_verbose():
        traceback.print_exception(e)
