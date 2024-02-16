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

from aurora_cli.src.features.devices.impl.common import common_command, common_run, common_install, common_upload
from aurora_cli.src.features.devices.impl.utils import device_ssh_select, get_ssh_client_device
from aurora_cli.src.support.helper import check_array_with_exit
from aurora_cli.src.support.output import echo_stderr, echo_stdout
from aurora_cli.src.support.texts import AppTexts


@click.group(name='device')
def group_device():
    """Working with the device."""
    pass


@group_device.command()
@click.pass_context
def available(ctx: {}):
    """Get available devices from configuration."""

    devices = check_array_with_exit(ctx.obj.get_devices(), AppTexts.devices_not_found())

    for ip, device in devices.items():
        if not get_ssh_client_device(ip, device['port'], device['pass']):
            echo_stderr(AppTexts.device_not_active(ip))
        else:
            echo_stdout(AppTexts.device_active(ip))


@group_device.command()
@click.pass_context
@click.option('-e', '--execute', type=click.STRING, required=True, help='The command to be executed on the device')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def command(ctx: {}, execute: str, index: int, verbose: bool):
    """Execute the command on the device."""

    # Get device client
    client, _ = device_ssh_select(ctx, index)

    # Run common with emulator function
    common_command(client, execute, ctx.obj.get_type_output(verbose))


@group_device.command()
@click.pass_context
@click.option('-p', '--package', type=click.STRING, required=True, help='Package name')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def run(ctx: {}, package: str, index: int, verbose: bool):
    """Run package on device in container."""

    # Get device client
    client, _ = device_ssh_select(ctx, index)

    # Run common with emulator function
    common_run(client, package, ctx.obj.get_type_output(verbose))


@group_device.command()
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def install(ctx: {}, path: [], index: int, verbose: bool):
    """Install RPM package on device."""

    # Get device client
    client, data = device_ssh_select(ctx, index)

    # Run common with emulator function
    common_install(client, path, data, ctx.obj.get_type_output(verbose))


@group_device.command()
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to file')
@click.option('-i', '--index', type=click.INT, help='Specify index')
def upload(ctx: {}, path: [], index: int):
    """Upload file to ~/Download directory device."""

    # Get device client
    client, _ = device_ssh_select(ctx, index)

    # Run common with emulator function
    common_upload(client, path)
