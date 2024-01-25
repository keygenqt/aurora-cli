import os

import click

from app.src.base.ssh import ssh_client_exec_command
from app.src.base.utils import get_full_path
from app.src.features.emulator.impl.ssh import get_ssh_client_vm, upload_file_sftp_vm
from app.src.features.emulator.impl.vbox import get_emulator_vm, run_emulator_vm


@click.group(name='emulator')
def group_emulator():
    """Working with the emulator virtualbox."""
    pass


@group_emulator.command()
def available():
    """Get available emulator."""

    emulator_name, emulator_key = get_emulator_vm()

    if emulator_name:
        emulator = emulator_name.replace('-base', '').split('-')
        click.echo('Emulator virtualbox Aurora OS: {}'.format(emulator[1]))
    else:
        click.echo('Emulator virtualbox not found.')


@group_emulator.command()
def startup():
    """Start emulator."""

    emulator_name, emulator_key = get_emulator_vm()

    if emulator_name:
        run_emulator_vm(emulator_key)
    else:
        click.echo('Emulator virtualbox not found.')


@group_emulator.command()
@click.option('-e', '--exec_command', type=click.STRING, required=True)
def command(exec_command):
    """Execute the command on the emulator."""

    # Get emulator client
    client = get_ssh_client_vm()

    # Check exist
    if not client:
        click.echo(click.style('The emulator is not active.', fg='red'))
        exit(1)

    # Run command
    ssh_stdout, ssh_stderr = ssh_client_exec_command(client, exec_command)

    # Show output
    if ssh_stdout:
        click.echo(ssh_stdout)
    if ssh_stderr:
        click.echo(ssh_stderr)


@group_emulator.command()
@click.option('-f', '--file_path', multiple=True, type=click.STRING, required=True)
def upload(file_path):
    """Upload file to ~/Download directory emulator."""

    # Get emulator client
    client = get_ssh_client_vm()

    # Check exist
    if not client:
        click.echo(click.style('The emulator is not active.', fg='red'))
        exit(1)

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    for file in file_path:
        # Get full path
        package_path = get_full_path(file)
        # Get file name
        file_name = os.path.basename(package_path)
        # Check exist and upload
        if package_path and upload_file_sftp_vm(upload_path, package_path):
            click.echo('{} {}'.format(click.style('Uploaded successfully:', fg='green'), file_name))
        else:
            click.echo('{} {}'.format(
                click.style('An error occurred while uploading the file: ', fg='red'), file), err=True)


@group_emulator.command()
@click.option('-f', '--file-path', multiple=True, type=click.STRING, required=True)
@click.option('-v', '--verbose', is_flag=True)
def install(file_path, verbose):
    """Install RPM package on emulator."""

    # Get emulator client
    client = get_ssh_client_vm(True)

    # Check exist
    if not client:
        click.echo(click.style('The emulator is not active.', fg='red'))
        exit(1)

    # Folder upload
    upload_path = '/home/defaultuser/Downloads'

    for package in file_path:
        # Get full path
        package_path = get_full_path(package, 'rpm')
        # Get file name
        file_name = os.path.basename(package_path)
        # Check exist and upload
        if package_path and upload_file_sftp_vm(upload_path, package_path):
            # Exec command
            exec_command = '{} {upload_path}/{file_name}'.format(
                'pkcon -y install-local',
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


@group_emulator.command()
@click.option('-p', '--package', type=click.STRING, required=True)
@click.option('-v', '--verbose', is_flag=True)
def run(package, verbose):
    """Run package on device in container."""

    # Get emulator client
    client = get_ssh_client_vm()

    # Check exist
    if not client:
        click.echo(click.style('The emulator is not active.', fg='red'))
        exit(1)

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
