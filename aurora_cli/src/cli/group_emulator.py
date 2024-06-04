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
from paramiko.client import SSHClient

from aurora_cli.src.base.common.vm_features import (
    vm_emulator_start,
    vm_emulator_screenshot,
    vm_emulator_record_start,
    vm_emulator_record_stop,
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.models.emulator_model import EmulatorModel
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.prompt import TextPrompt
from aurora_cli.src.base.utils.abort import abort_catch, abort_text_start, abort_text_end
from aurora_cli.src.base.utils.argv import argv_is_test
from aurora_cli.src.base.utils.output import echo_stdout
from aurora_cli.src.cli.impl.ssh_commands import (
    ssh_common_command_cli,
    ssh_common_run_cli,
    ssh_common_upload_cli,
    ssh_common_install_cli,
    ssh_common_remove_cli
)


def _get_emulator_model(
        is_root: bool
) -> EmulatorModel:
    if is_root:
        return EmulatorModel.get_model_root()
    else:
        return EmulatorModel.get_model_user()


def _get_emulator_ssh_client(verbose: bool, is_root: bool = False) -> SSHClient:
    result = _get_emulator_model(is_root).get_ssh_client()
    if result.is_error():
        echo_stdout(result, verbose)
        exit(1)
    return result.value


@click.group(name='emulator', help=TextGroup.group_emulator())
@click.pass_context
def group_emulator(ctx: {}):
    if argv_is_test():
        ctx.obj = AppConfig.create_test()


@group_emulator.command(name='start', help=TextCommand.command_emulator_start())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def vm_emulator_start_cli(verbose: bool):
    echo_stdout(vm_emulator_start(), verbose)


@group_emulator.command(name='screenshot', help=TextCommand.command_emulator_screenshot())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def vm_emulator_screenshot_cli(verbose: bool):
    echo_stdout(vm_emulator_screenshot(), verbose)


@group_emulator.command(name='recording', help=TextCommand.command_emulator_recording())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def vm_emulator_record_cli(verbose: bool):
    result = vm_emulator_record_start()
    echo_stdout(result, verbose)
    if result.is_error():
        exit(1)

    def stop_record_and_exit():
        print('')
        abort_text_start()
        vm_emulator_record_stop()
        abort_text_end()
        exit(0)

    abort_catch(lambda: stop_record_and_exit())
    click.prompt(
        text=TextPrompt.emulator_recording_video_loading(),
        prompt_suffix='',
        default='Enter',
        hide_input=True
    )
    echo_stdout(vm_emulator_record_stop(), verbose)


@group_emulator.command(name='command', help=TextCommand.command_emulator_command())
@click.option('-e', '--execute', type=click.STRING, required=True, help=TextArgument.argument_execute_emulator())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_emulator_command_cli(execute: str, verbose: bool):
    ssh_common_command_cli(
        client=_get_emulator_ssh_client(verbose),
        execute=execute,
        verbose=verbose
    )


@group_emulator.command(name='upload', help=TextCommand.command_emulator_upload())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_emulator_upload_cli(path: [], verbose: bool):
    ssh_common_upload_cli(
        client=_get_emulator_ssh_client(verbose),
        path=path,
        verbose=verbose
    )


@group_emulator.command(name='package-run', help=TextCommand.command_emulator_package_run())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-n', '--nohup', is_flag=True, help=TextArgument.argument_exit_after_run())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_emulator_run_cli(package: str, nohup: bool, verbose: bool):
    ssh_common_run_cli(
        client=_get_emulator_ssh_client(verbose),
        package=package,
        nohup=nohup,
        verbose=verbose
    )


@group_emulator.command(name='package-install', help=TextCommand.command_emulator_package_install())
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help=TextArgument.argument_path_rpm())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_emulator_install_cli(path: [], apm: bool, verbose: bool):
    ssh_common_install_cli(
        client=_get_emulator_ssh_client(verbose, True),
        path=path,
        apm=apm,
        verbose=verbose
    )


@group_emulator.command(name='package-remove', help=TextCommand.command_emulator_package_remove())
@click.option('-p', '--package', type=click.STRING, required=True, help=TextArgument.argument_package_name())
@click.option('-a', '--apm', is_flag=True, help=TextArgument.argument_apm())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def ssh_emulator_remove_cli(package: str, apm: bool, verbose: bool):
    ssh_common_remove_cli(
        client=_get_emulator_ssh_client(verbose, True),
        package=package,
        apm=apm,
        verbose=verbose
    )
