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

from aurora_cli.src.features.devices.group_emulator_vm import emulator_start, emulator_screenshot, emulator_recording
from aurora_cli.src.features.devices.impl.common import common_command, common_run, common_install, common_upload
from aurora_cli.src.features.devices.impl.utils import emulator_ssh_select


@click.group(name='emulator')
def group_emulator():
    """Working with the emulator virtualbox."""
    pass


# Add subgroup
group_emulator.add_command(emulator_start)
group_emulator.add_command(emulator_screenshot)
group_emulator.add_command(emulator_recording)


@group_emulator.command()
@click.pass_context
@click.option('-e', '--execute', type=click.STRING, required=True, help='The command to be executed on the emulator')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def command(ctx: {}, execute: str, verbose: bool):
    """Execute the command on the emulator."""

    client = emulator_ssh_select()

    # Run common with emulator function
    common_command(client, execute, ctx.obj.get_type_output(verbose))


@group_emulator.command()
@click.pass_context
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def run(ctx: {}, package: str, verbose: bool):
    """Run package on emulator in container."""

    # Get emulator client
    client = emulator_ssh_select()

    # Run common with emulator function
    common_run(client, package, ctx.obj.get_type_output(verbose))


@group_emulator.command()
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def install(ctx: {}, path: [], verbose: bool):
    """Install RPM package on emulator."""

    # Get emulator client
    client = emulator_ssh_select(is_root=True)

    # Run common with emulator function
    common_install(client, path, {}, ctx.obj.get_type_output(verbose))


@group_emulator.command()
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to file')
def upload(path: []):
    """Upload file to ~/Download directory emulator."""

    # Get emulator client
    client = emulator_ssh_select()

    # Run common with emulator function
    common_upload(client, path)
