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
from datetime import datetime
from pathlib import Path

import click

from aurora_cli.src.features.devices.impl.common import common_command, common_run, common_install, common_upload
from aurora_cli.src.features.devices.impl.utils import emulator_ssh_select
from aurora_cli.src.support.output import VerboseType, echo_stdout
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.vbox import vm_search_emulator_aurora, vb_manage_command, vm_check_is_run


@click.group(name='emulator')
def group_emulator():
    """Working with the emulator virtualbox."""
    pass


@group_emulator.command()
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def start(verbose: bool):
    """Start emulator."""

    emulator_name = vm_search_emulator_aurora(verbose)

    if vm_check_is_run(emulator_name):
        echo_stdout(AppTexts.vm_already_running())
    else:
        vb_manage_command(
            ['startvm', emulator_name],
            VerboseType.true if verbose else VerboseType.false,
            ['.+error.+']
        )


@group_emulator.command()
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def screenshot(verbose: bool):
    """Take screenshot emulator."""

    emulator_name = vm_search_emulator_aurora(verbose)

    if vm_check_is_run(emulator_name):
        # Screenshot path directory
        screenshot_dir = Path.home() / 'Pictures' / 'Screenshots'

        # Create is not exist
        if screenshot_dir.is_dir():
            screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Screenshot name
        screenshot_name = 'Screenshot_from_{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

        # Run command for take screenshot
        vb_manage_command(
            ['controlvm', emulator_name, 'screenshotpng', str(screenshot_dir / screenshot_name)],
            VerboseType.true if verbose else VerboseType.false,
        )
    else:
        echo_stdout(AppTexts.vm_is_not_running())


@group_emulator.command()
@click.option('-e', '--execute', type=click.STRING, required=True, help='The command to be executed on the emulator')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def command(execute: str, verbose: bool):
    """Execute the command on the emulator."""

    client = emulator_ssh_select()

    # Run common with emulator function
    common_command(client, execute, verbose)


@group_emulator.command()
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def run(package: str, verbose: bool):
    """Run package on emulator in container."""

    # Get emulator client
    client = emulator_ssh_select()

    # Run common with emulator function
    common_run(client, package, verbose)


@group_emulator.command()
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def install(path: [], verbose: bool):
    """Install RPM package on emulator."""

    # Get emulator client
    client = emulator_ssh_select(is_root=True)

    # Run common with emulator function
    common_install(client, path, {}, verbose)


@group_emulator.command()
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to file')
def upload(path: []):
    """Upload file to ~/Download directory emulator."""

    # Get emulator client
    client = emulator_ssh_select()

    # Run common with emulator function
    common_upload(client, path)
