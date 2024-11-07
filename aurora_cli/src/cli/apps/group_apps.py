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

import click

from aurora_cli.src.base.common.groups.apps.apps_features import apps_available_common
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose


@click.group(name='apps', help=TextGroup.group_apps())
def group_apps():
    AppConfig.create_test()


@group_apps.command(name='available', help=TextCommand.command_apps_available())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def available(verbose: bool):
    apps_available_common()
    echo_verbose(verbose)
