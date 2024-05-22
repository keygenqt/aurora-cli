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

from aurora_cli.src.base.output import echo_stdout
from aurora_cli.src.base.texts.prompt import TextPrompt
from aurora_cli.src.cli.ssh_commands import (
    ssh_common_command_cli,
    ssh_common_run_cli,
    ssh_common_upload_cli,
    ssh_common_install_cli,
    ssh_common_remove_cli
)
from aurora_cli.src.common.vm_features import (
    vm_emulator_start,
    vm_emulator_screenshot,
    vm_emulator_record_start,
    vm_emulator_record_stop,
)


def _get_emulator_ssh_client(verbose: bool) -> SSHClient:
    result = vm_emulator_record_start()
    echo_stdout(result, verbose)
    if result.is_error():
        exit(1)
    return result.value


@click.group(name='emulator')
def group_emulator():
    """Working with the emulator virtualbox."""
    pass


@group_emulator.command(name='start')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def vm_emulator_start_cli(verbose: bool):
    """Start emulator."""
    echo_stdout(vm_emulator_start(), verbose)


@group_emulator.command(name='screenshot')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def vm_emulator_screenshot_cli(verbose: bool):
    """Emulator take screenshot."""
    echo_stdout(vm_emulator_screenshot(), verbose)


@group_emulator.command(name='recording')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def vm_emulator_record_cli(verbose: bool):
    """Recording video from emulator."""
    result = vm_emulator_record_start()
    echo_stdout(result, verbose)
    if result.is_error():
        exit(1)
    click.prompt(
        text=TextPrompt.emulator_recording_video_loading(),
        prompt_suffix='',
        default='Enter',
        hide_input=True
    )
    echo_stdout(vm_emulator_record_stop(), verbose)


@group_emulator.command(name='command')
@click.option('-e', '--execute', type=click.STRING, required=True, help='The command to be executed on the emulator')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_command_cli(execute: str, verbose: bool):
    """Execute the command on the emulator."""
    ssh_common_command_cli(
        client=_get_emulator_ssh_client(verbose),
        execute=execute,
        verbose=verbose
    )


@group_emulator.command(name='run')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_run_cli(package: str, verbose: bool):
    """Run package on emulator in container."""
    ssh_common_run_cli(
        client=_get_emulator_ssh_client(verbose),
        package=package,
        verbose=verbose
    )


@group_emulator.command(name='upload')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to file')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_upload_cli(path: [], verbose: bool):
    """Upload file to ~/Download directory emulator."""
    ssh_common_upload_cli(
        client=_get_emulator_ssh_client(verbose),
        path=path,
        verbose=verbose
    )


@group_emulator.command(name='package-install')
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_install_cli(path: [], apm: bool, verbose: bool):
    """Install RPM package on emulator."""
    ssh_common_install_cli(
        client=_get_emulator_ssh_client(verbose),
        path=path,
        apm=apm,
        verbose=verbose
    )


@group_emulator.command(name='package-remove')
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-a', '--apm', is_flag=True, help='Use new install APM')
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def ssh_emulator_remove_cli(package: str, apm: bool, verbose: bool):
    """Install RPM package on emulator."""
    ssh_common_remove_cli(
        client=_get_emulator_ssh_client(verbose),
        package=package,
        apm=apm,
        verbose=verbose
    )
