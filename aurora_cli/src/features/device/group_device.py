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
import os

import click

from aurora_cli.src.base.ssh import ssh_client_exec_command
from aurora_cli.src.base.utils import get_string_from_list, get_full_path_file
from aurora_cli.src.features.device.impl.ssh import get_ssh_clients, prompt_ssh_client_device, upload_file_sftp


@click.group(name='device')
def group_device():
    """Working with the device."""
    pass


@group_device.command()
@click.pass_context
def available(ctx):
    """Get available devices from configuration."""

    devices = ctx.obj.get_devices()

    # Get connections
    clients = get_ssh_clients(devices)

    # Output
    if clients:
        click.echo('Available devices:\n{}'
                   .format(get_string_from_list(clients.keys())))
    else:
        click.echo('No active devices found.')


@group_device.command()
@click.pass_context
@click.option('-e', '--execute', type=click.STRING, required=True)
@click.option('-i', '--index', type=click.INT)
def command(ctx, execute, index):
    """Execute the command on the device."""

    # Get device client
    device, client = prompt_ssh_client_device(ctx, index)

    # Run command
    ssh_stdout, ssh_stderr = ssh_client_exec_command(client, execute)

    # Show output
    if ssh_stdout:
        click.echo(ssh_stdout)
    if ssh_stderr:
        click.echo(ssh_stderr)


@group_device.command()
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True)
@click.option('-i', '--index', type=click.INT)
def upload(ctx, path, index):
    """Upload file to ~/Download directory device."""

    # Get device client
    device, client = prompt_ssh_client_device(ctx, index)

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    for file in path:
        # Get full path
        package_path = get_full_path_file(file)
        # Get file name
        file_name = os.path.basename(package_path)
        # Check exist and upload
        if package_path and upload_file_sftp(ctx, device, upload_path, package_path):
            click.echo('{} {}'.format(click.style('Uploaded successfully:', fg='green'), file_name))
        else:
            click.echo('{} {}'.format(
                click.style('An error occurred while uploading the file: ', fg='red'), file), err=True)


@group_device.command()
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True)
@click.option('-i', '--index', type=click.INT)
@click.option('-s', '--devel-su', type=click.STRING)
@click.option('-v', '--verbose', is_flag=True)
def install(ctx, path, index, devel_su, verbose):
    """Install RPM package on device."""

    # Get device client
    device, client = prompt_ssh_client_device(ctx, index)

    # Get pass root
    if not devel_su:
        devel_su = ctx.obj.get_devices()[device]['devel-su']

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    for package in path:
        # Get full path
        package_path = get_full_path_file(package, 'rpm')
        # Get file name
        file_name = os.path.basename(package_path)
        # Check exist and upload
        if package_path and upload_file_sftp(ctx, device, upload_path, package_path):
            # Exec command
            exec_command = 'echo {} | {} {upload_path}/{file_name}'.format(
                devel_su,
                'devel-su pkcon -y install-local',
                upload_path=upload_path,
                file_name=file_name
            )
            # Run command
            ssh_stdout, ssh_stderr = ssh_client_exec_command(client, exec_command)
            # Show output
            if verbose:
                if ssh_stdout:
                    click.echo(ssh_stdout)
                if ssh_stderr:
                    click.echo(ssh_stderr)
            else:
                if 'error' in ssh_stdout:
                    click.echo('{} {}\n{}'.format(click.style('Error installing package: ', fg='red'),
                                                  file_name,
                                                  'For the report you can add (-v) --verbose'), err=True)
                else:
                    click.echo('{} {}'.format(click.style('Installed successfully:', fg='green'), file_name))
        else:
            click.echo('{} {}'.format(
                click.style('An error occurred while uploading the file: ', fg='red'), package), err=True)


@group_device.command()
@click.pass_context
@click.option('-p', '--package', type=click.STRING, required=True)
@click.option('-i', '--index', type=click.INT)
@click.option('-v', '--verbose', is_flag=True)
def run(ctx, package, index, verbose):
    """Run package on device in container."""

    # Get device client
    device, client = prompt_ssh_client_device(ctx, index)

    # Exec command
    exec_command = 'invoker --type=qt5 {package}'.format(package=package)

    # Run command
    _, ssh_stdout, ssh_stderr = client.exec_command(exec_command, get_pty=True)

    # Output
    for line in iter(ssh_stdout.readline, ""):
        line = str(line).strip()
        if verbose:
            click.echo(line)
        if 'died' in line and not verbose:
            click.echo('{} {}\n{}'.format(click.style('Error run package:', fg='red'),
                                          package,
                                          'For the report you can add (-v) --verbose'), err=True)
            exit(1)
