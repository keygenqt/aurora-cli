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

from aurora_cli.src.base.common.groups.emulator_features import (
    emulator_start_common,
    emulator_command_common,
    emulator_upload_common,
    emulator_package_run_common,
    emulator_package_install_common,
    emulator_package_remove_common,
    emulator_recording_start_common,
    emulator_recording_stop_common,
    emulator_screenshot_common,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.prompt import TextPrompt
from aurora_cli.src.base.utils.abort import abort_catch, abort_text_start, abort_text_end
from aurora_cli.src.base.utils.argv import argv_is_test


def _select_model(
        verbose: bool,
        is_root: bool = False,
) -> EmulatorModel:
    if is_root:
        return EmulatorModel.get_model_root(verbose)
    else:
        return EmulatorModel.get_model_user(verbose)


@click.group(name='emulator', help=TextGroup.group_emulator())
@click.pass_context
def group_emulator(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_emulator.command(name='start', help=TextCommand.command_emulator_start())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def start(verbose: bool):
    model = _select_model(verbose)
    emulator_start_common(model, verbose)


@group_emulator.command(name='screenshot', help=TextCommand.command_emulator_screenshot())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def screenshot(verbose: bool):
    model = _select_model(verbose)
    emulator_screenshot_common(model, verbose)


@group_emulator.command(name='recording', help=TextCommand.command_emulator_recording())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def recording(verbose: bool):
    model = _select_model(verbose)
    emulator_recording_start_common(model, verbose)

    def stop_record_and_exit():
        print('')
        abort_text_start()
        emulator_recording_stop_common(model, verbose)
        abort_text_end()
        exit(0)

    abort_catch(lambda: stop_record_and_exit())

    click.prompt(
        text=TextPrompt.emulator_recording_video_loading(),
        prompt_suffix='',
        default='Enter',
        hide_input=True
    )
    emulator_recording_stop_common(model, verbose)


@group_emulator.command(name='command', help=TextCommand.command_emulator_command())
@click.option('-e', '--execute', type=click.STRING, required=True, help=TextArgument.argument_execute_emulator())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def command(execute: str, verbose: bool):
    model = _select_model(verbose)
    emulator_command_common(model, execute, verbose)


@group_emulator.command(name='upload', help=TextCommand.command_emulator_upload())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def upload(path: [], verbose: bool):
    model = _select_model(verbose)
    emulator_upload_common(model, path, verbose)


@group_emulator.command(name='package-run', help=TextCommand.command_emulator_package_run())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_run(package: str, verbose: bool):
    model = _select_model(verbose)
    emulator_package_run_common(model, package, verbose)


@group_emulator.command(name='package-install', help=TextCommand.command_emulator_package_install())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_install(path: [], apm: bool, verbose: bool):
    model = _select_model(verbose, True)
    emulator_package_install_common(model, path, apm, verbose)


@group_emulator.command(name='package-remove', help=TextCommand.command_emulator_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def package_remove(package: str, apm: bool, verbose: bool):
    model = _select_model(verbose, True)
    emulator_package_remove_common(model, package, apm, verbose)
