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

from aurora_cli.src.base.common.groups.settings.settings_features import (
    settings_list_common,
    settings_clear_common,
    settings_localization_common,
    settings_verbose_common,
    settings_select_common,
    settings_hint_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.utils.output import echo_verbose


@click.group(name='settings', help=TextGroup.group_settings())
def group_settings():
    AppConfig.create_test()


@group_settings.command(name='list', help=TextCommand.command_settings_list())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def settings_list(verbose: bool):
    settings_list_common()
    echo_verbose(verbose)


@group_settings.command(name='clear', help=TextCommand.command_settings_clear())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def settings_clear(verbose: bool):
    settings_clear_common()
    echo_verbose(verbose)


@group_settings.command(name='localization', help=TextCommand.command_settings_localization())
@click.option('-l', '--language', type=click.Choice(['ru', 'en']), required=True, help=TextArgument.argument_language())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def settings_localization(language: str, verbose: bool):
    settings_localization_common(language)
    echo_verbose(verbose)


@group_settings.command(name='verbose', help=TextCommand.command_settings_verbose())
@click.option('-e', '--enable', type=click.Choice(['true', 'false']), required=True,
              help=TextArgument.argument_enable_verbose())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def settings_verbose(enable: str, verbose: bool):
    settings_verbose_common(enable == 'true')
    echo_verbose(verbose)


@group_settings.command(name='select', help=TextCommand.command_settings_select())
@click.option('-e', '--enable', type=click.Choice(['true', 'false']), required=True,
              help=TextArgument.argument_enable_save_select())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def settings_select(enable: str, verbose: bool):
    settings_select_common(enable == 'true')
    echo_verbose(verbose)


@group_settings.command(name='hint', help=TextCommand.command_settings_hint())
@click.option('-e', '--enable', type=click.Choice(['true', 'false']), required=True,
              help=TextArgument.argument_enable_hint())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def settings_select(enable: str, verbose: bool):
    settings_hint_common(enable == 'true')
    echo_verbose(verbose)
