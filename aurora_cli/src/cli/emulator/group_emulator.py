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

from aurora_cli.src.base.common.groups.emulator.emulator_features import (
    emulator_command_common,
    emulator_upload_common,
    emulator_start_common,
    emulator_screenshot_common,
    emulator_recording_start_common,
    emulator_recording_stop_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.localization.localization import localization_abort_start, localization_abort_end
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.prompt import TextPrompt
from aurora_cli.src.base.utils.app import app_abort_handler
from aurora_cli.src.base.utils.output import echo_verbose
from aurora_cli.src.cli.emulator.__tools import cli_emulator_tool_select_model
from aurora_cli.src.cli.emulator.subgroup_emulator_package import subgroup_emulator_package


# noinspection PyTypeChecker
def init_subgroups_emulator():
    group_emulator.add_command(subgroup_emulator_package)


@click.group(name='emulator', help=TextGroup.group_emulator())
def group_emulator():
    AppConfig.create_test()


@group_emulator.command(name='command', help=TextCommand.command_emulator_command())
@click.option('-e', '--execute', type=click.STRING, required=True, help=TextArgument.argument_execute_emulator())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def command(
        execute: str,
        verbose: bool
):
    model = cli_emulator_tool_select_model()
    emulator_command_common(model, execute)
    echo_verbose(verbose)


@group_emulator.command(name='upload', help=TextCommand.command_emulator_upload())
@click.option('-p', '--path', type=click.STRING, required=True, help=TextArgument.argument_path())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def upload(
        path: str,
        verbose: bool
):
    model = cli_emulator_tool_select_model()
    emulator_upload_common(model, path)
    echo_verbose(verbose)


@group_emulator.command(name='start', help=TextCommand.command_emulator_start())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def start(verbose: bool):
    model = cli_emulator_tool_select_model()
    emulator_start_common(model)
    echo_verbose(verbose)


@group_emulator.command(name='screenshot', help=TextCommand.command_emulator_screenshot())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def screenshot(verbose: bool):
    model = cli_emulator_tool_select_model()
    emulator_screenshot_common(model)
    echo_verbose(verbose)


@group_emulator.command(name='recording', help=TextCommand.command_emulator_recording())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def recording(verbose: bool):
    model = cli_emulator_tool_select_model()
    emulator_recording_start_common(model)
    model = cli_emulator_tool_select_model()

    def stop_record_and_exit():
        print('')
        localization_abort_start()
        emulator_recording_stop_common(model, save=False)
        localization_abort_end()
        exit(0)

    app_abort_handler(lambda: stop_record_and_exit())

    click.prompt(
        text=TextPrompt.emulator_recording_video_loading(),
        prompt_suffix='',
        default='Enter',
        hide_input=True
    )
    emulator_recording_stop_common(model, save=True)
    echo_verbose(verbose)
