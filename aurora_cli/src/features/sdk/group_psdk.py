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
import getpass
import os
import pathlib
import subprocess
from pathlib import Path

import click
from cffi.backend_ctypes import unicode

from aurora_cli.src.base.utils import get_string_from_list, get_string_from_list_numbered, prompt_index, \
    bar_subprocess_lines, bar_subprocess_symbol, move_root_file, update_file_lines, get_full_path_file, get_full_path
from aurora_cli.src.features.sdk.impl.download import multi_download
from aurora_cli.src.features.sdk.impl.psdk import get_list_psdk_installed, MER_SDK_CHROOT, SDK_CHROOT, SDK_CHROOT_DATA, \
    MER_SDK_CHROOT_DATA, check_sudoers_chroot, get_list_targets
from aurora_cli.src.features.sdk.impl.urls import get_map_versions, TypeSDK, get_urls_on_html


@click.group(name='psdk')
def group_psdk():
    """Working with the Aurora Platform SDK."""
    pass


@group_psdk.command()
def available():
    """Get available version Aurora Platform SDK."""

    versions = get_map_versions(TypeSDK.PSDK)

    click.echo('Available Aurora Platform SDK versions:\n{}'
               .format(get_string_from_list(versions.keys())))


@group_psdk.command()
@click.option('-l', '--latest', is_flag=True, help="Select latest version")
def install(latest):
    """Download and install Aurora Platform SDK."""

    # Load versions
    versions = get_map_versions(TypeSDK.PSDK)

    if not latest:
        # Query index
        click.echo('Select index Aurora Platform SDK versions:\n{}'
                   .format(get_string_from_list_numbered(versions.keys())))
        index = prompt_index(versions.keys())
        key = list(versions.keys())[index - 1]
    else:
        key = list(versions.keys())[0]

    # Variables
    url = '{}{}'.format(versions[key], key)
    links = get_urls_on_html(url)
    files = [item for item in links if 'md5sum' not in item]
    files_url = ['{}{}'.format(url, item) for item in files]

    # Download files
    click.echo('')
    files = multi_download(files_url)

    # Find archive
    archive_chroot = [item for item in files if 'Chroot' in item and 'tar.bz2' in item]
    archive_tooling = [item for item in files if 'Tooling' in item]
    archive_target = [item for item in files if 'Target' in item]

    # Check exist chroot
    if not archive_chroot:
        click.echo(click.style('Error: Chroot tar.bz2 not found.', fg='red'), err=True)
        return

    # Check exist tooling
    if not archive_tooling:
        click.echo(click.style('Error: Tooling tar.bz2 not found.', fg='red'), err=True)
        return

    # Get version psdk
    version = os.path.basename(archive_chroot[0]).split('-')[1]

    # Get path for install
    path_psdk = str(Path.home() / 'Aurora_Platform_SDK_{}'.format(version))
    path_chroot = '{}/sdks/aurora_psdk'.format(path_psdk)

    # Chroot path
    chroot = '{}/sdk-chroot'.format(path_chroot)

    # Check psdk already folder exist
    if os.path.isdir(path_psdk):
        click.echo(click.style('\nError: Folder already exists: {}'.format(path_psdk), fg='red'), err=True)
        return

    # Get root permissions
    subprocess.call(['sudo', 'echo'])

    # Create folders
    pathlib.Path(path_psdk).mkdir()
    pathlib.Path(path_chroot).mkdir(parents=True, exist_ok=True)
    pathlib.Path('{}/toolings'.format(path_psdk)).mkdir()
    pathlib.Path('{}/tarballs'.format(path_psdk)).mkdir()
    pathlib.Path('{}/targets'.format(path_psdk)).mkdir()

    # Install chroot with progress
    click.echo('Install chroot')
    with subprocess.Popen([
        'sudo',
        'tar',
        '--numeric-owner',
        '-p',
        '-xjf',
        archive_chroot[0],
        '--blocking-factor=20',
        '--record-size=512',
        '--checkpoint=.10',
        '-C',
        path_chroot
    ], stdout=subprocess.PIPE) as process:
        # Ref size - 273205534 (bytes) == 175726 (checkpoint)
        archive_size = os.stat(archive_chroot[0]).st_size
        bar_subprocess_symbol(int(175726 * archive_size / 273205534), process)

    # Install tooling with progress
    click.echo('Install tooling')
    with subprocess.Popen([
        chroot,
        'sdk-assistant',
        'tooling',
        'create',
        '-y',
        'AuroraOS-{}-base'.format(version),
        archive_tooling[0]
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        # Ref size - 10 output lines
        bar_subprocess_lines(10, process)

    # Install targets with progress
    for target in archive_target:
        arch = target.split('-')[-1].split('.')[0]
        click.echo('Install target "{}"'.format(arch))
        with subprocess.Popen([
            chroot,
            'sdk-assistant',
            'target',
            'create',
            '-y',
            'AuroraOS-{}-base-{}'.format(version, arch),
            target
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            # Ref size - 25 output lines
            bar_subprocess_lines(25, process)

    click.echo("""
{successfully}
    
You should update your ~/.bashrc to include export:

    {psdk_dir}

Add alias for convenience:

    {psdk_alias}

After that run the command:

    {source}

You can check the installation with the command:

    {list}

The files have been downloaded to the ~/Downloads folder, if you no longer need them, delete them.

Good luck!""".format(
        successfully=click.style(
            'Install Aurora Platform SDK "{}" successfully!'.format(version),
            fg='green'
        ),
        psdk_dir=click.style(
            'export PSDK_DIR=$HOME/Aurora_Platform_SDK_{}/sdks/aurora_psdk'.format(version),
            fg='blue'
        ),
        psdk_alias=click.style(
            'alias aurora_psdk=$HOME/Aurora_Platform_SDK_{}/sdks/aurora_psdk/sdk-chroot'.format(version),
            fg='blue'
        ),
        source=click.style(
            'source $HOME/.bashrc',
            fg='blue'
        ),
        list=click.style(
            'aurora_psdk sdk-assistant list',
            fg='blue'
        ),
    ))


@group_psdk.command()
def installed():
    """Get installed list Aurora Platform SDK."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    click.echo('Found the installed Aurora Platform SDK:\n{}'
               .format(get_string_from_list(psdks.keys())))


@group_psdk.command()
def remove():
    """Remove installed Aurora Platform SDK."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    if len(psdks.keys()) != 1:
        click.echo('Found the installed Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(psdks.keys())))

    # Query index
    index = prompt_index(psdks.keys())
    key = list(psdks.keys())[index - 1]

    # Path psdk folder
    path = Path.home() / key

    if not click.confirm('\nDo you want to continue?\nThe path folder will be deleted: {}'.format(path)):
        return

    # Remove folder psdk
    subprocess.call([
        'sudo',
        'rm',
        '-rf',
        path
    ])

    # Clear .bashrc
    with open(Path.home() / '.bashrc', 'r') as f:
        lines = f.readlines()
    with open(Path.home() / '.bashrc', 'w') as f:
        for line in lines:
            if key not in line:
                f.write(line)

    # Clear /etc/sudoers.d/mer-sdk-chroot
    path = update_file_lines(MER_SDK_CHROOT, key)
    move_root_file(path, MER_SDK_CHROOT)

    # Clear /etc/sudoers.d/sdk-chroot
    path = update_file_lines(SDK_CHROOT, key)
    move_root_file(path, SDK_CHROOT)

    click.echo(click.style(
        'Remove Aurora Platform SDK successfully!',
        fg='green'
    ))


@group_psdk.command()
@click.option('-d', '--delete', is_flag=True, default=False, required=True, help="Enable remove sudoers permissions.")
def sudoers(delete):
    """Add sudoers permissions Aurora Platform SDK."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    if len(psdks.keys()) != 1:
        click.echo('Found the installed Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(psdks.keys())))

    # Query index
    index = prompt_index(psdks.keys())
    key = list(psdks.keys())[index - 1]
    psdk_dir = os.path.dirname(psdks[key])

    if delete:
        # Clear /etc/sudoers.d/mer-sdk-chroot
        path = update_file_lines(MER_SDK_CHROOT, key)
        move_root_file(path, MER_SDK_CHROOT)

        # Clear /etc/sudoers.d/sdk-chroot
        path = update_file_lines(SDK_CHROOT, key)
        move_root_file(path, SDK_CHROOT)

        click.echo('{}{}{}'.format(click.style('Delete for "', fg='green'),
                                   key,
                                   click.style('" sudoers permissions successfully!', fg='green')))
    else:
        # Update /etc/sudoers.d/mer-sdk-chroot
        insert = MER_SDK_CHROOT_DATA.format(username=getpass.getuser(), psdk_dir=psdk_dir)
        path = update_file_lines(MER_SDK_CHROOT, key, insert=insert)
        move_root_file(path, MER_SDK_CHROOT)

        # Update /etc/sudoers.d/sdk-chroot
        insert = SDK_CHROOT_DATA.format(username=getpass.getuser(), psdk_dir=psdk_dir)
        path = update_file_lines(SDK_CHROOT, key, insert=insert)
        move_root_file(path, SDK_CHROOT)

        click.echo('{}{}{}'.format(click.style('Added for "', fg='green'),
                                   key,
                                   click.style('" sudoers permissions successfully!', fg='green')))


@group_psdk.command()
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True)
@click.option('-i', '--index', type=click.INT)
@click.option('-k', '--key-path', type=click.STRING)
@click.option('-c', '--cert-path', type=click.STRING)
@click.option('-v', '--verbose', is_flag=True)
def sign(ctx, path, index, key_path, cert_path, verbose):
    """Sign (with re-sign) RPM package."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    if len(psdks.keys()) != 1:
        click.echo('Found the installed Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(psdks.keys())))

    # Query index
    r_index = prompt_index(psdks.keys(), index)
    key_psdk = list(psdks.keys())[r_index - 1]

    # Chroot
    chroot = psdks[key_psdk]

    # Get keys from configuration
    if not key_path or not cert_path:
        keys = ctx.obj.get_keys()
        if len(keys.keys()) != 1:
            click.echo('Signature keys found:\n{}'
                       .format(get_string_from_list_numbered(keys.keys())))
        r_index = prompt_index(keys.keys(), index)
        key_name = list(keys.keys())[r_index - 1]
        if not key_path:
            key_path = keys[key_name]['key']
        if not cert_path:
            cert_path = keys[key_name]['cert']

    # Update path
    key_path = get_full_path(key_path)
    cert_path = get_full_path(cert_path)

    # Check and query root permission
    check_sudoers_chroot(key_psdk)

    for package in path:
        # Get full path
        package_path = get_full_path_file(package, 'rpm')
        # Check exist and rpm extension
        if package_path:

            # Remove if exist sign
            subprocess.Popen([
                chroot,
                'rpmsign-external',
                'delete',
                package_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Add sign
            output, err = subprocess.Popen([
                chroot,
                'rpmsign-external',
                'sign',
                '--key',
                key_path,
                '--cert',
                cert_path,
                package_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

            if verbose:
                if output:
                    click.echo(output)
                if err:
                    click.echo(err)
            else:
                if 'Signed' in str(err):
                    click.echo('{} {}'.format(click.style('Signed successfully:', fg='green'), package))
                elif 'Could not open' in str(err):
                    click.echo('{} {}'.format(
                        click.style('Could not open certificate or private key.\nCheck the configuration file:',
                                    fg='red'),
                        ctx.obj.get_path()), err=True)
                else:
                    click.echo('{} {}'.format(click.style('Could not sign:', fg='red'), package), err=True)


@group_psdk.command()
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True)
@click.option('-v', '--verbose', is_flag=True)
def validate(path, verbose):
    """Validate RPM packages."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    if len(psdks.keys()) != 1:
        click.echo('Found the installed Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(psdks.keys())))

    # Query index
    r_index = prompt_index(psdks.keys())
    key = list(psdks.keys())[r_index - 1]

    # Chroot
    chroot = psdks[key]

    # Check and query root permission
    check_sudoers_chroot(key)

    # Get psdk targets
    targets = get_list_targets(chroot)

    if not targets:
        click.echo('Targets in Aurora Platform SDK not found.')
        return

    if len(targets) != 1:
        click.echo('Found targets Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(targets)))

    # Query index
    r_index = prompt_index(targets)
    target = list(targets)[r_index - 1]

    for package in path:
        # Get full path
        package_path = get_full_path_file(package, 'rpm')
        # Has error
        is_error = False
        # Check exist and rpm extension
        if package_path:
            # Get file name
            file_name = os.path.basename(package_path)
            # Run validate
            with subprocess.Popen([
                chroot,
                'sb2',
                '-t',
                target,
                '-m',
                'emulate',
                'rpm-validator',
                package_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                for line in iter(lambda: process.stderr.readline(), ""):
                    if not line:
                        break
                    line = unicode(line.rstrip(), "utf-8")
                    if verbose:
                        click.echo(line)
                    else:
                        if 'ERROR' in line:
                            is_error = True
                            click.echo('{} {}'.format(
                                click.style('ERROR:', fg='red'), line.replace('(ERROR)', '').strip()), err=True)
                if not is_error and not verbose:
                    click.echo('{} {}'.format(click.style('Validation completed successfully:', fg='green'), file_name))


@group_psdk.command()
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True)
@click.option('-v', '--verbose', is_flag=True)
def sdk_install(path, verbose):
    """Install RPM packages to target."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    if len(psdks.keys()) != 1:
        click.echo('Found the installed Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(psdks.keys())))

    # Query index
    r_index = prompt_index(psdks.keys())
    key = list(psdks.keys())[r_index - 1]

    # Chroot
    chroot = psdks[key]

    # Check and query root permission
    check_sudoers_chroot(key)

    # Get psdk targets
    targets = get_list_targets(chroot)

    if not targets:
        click.echo('Targets in Aurora Platform SDK not found.')
        return

    if len(targets) != 1:
        click.echo('Found targets Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(targets)))

    # Query index
    r_index = prompt_index(targets)
    target = list(targets)[r_index - 1]

    for package in path:
        # Get full path
        package_path = get_full_path_file(package, 'rpm')
        # Has error
        is_error = False
        # Check exist and rpm extension
        if package_path:
            # Get file name
            file_name = os.path.basename(package_path)
            # Run execute
            with subprocess.Popen([
                chroot,
                'sb2',
                '-t',
                target,
                '-m',
                'sdk-install',
                '-R',
                'zypper',
                '--no-gpg-checks',
                'in',
                '-y',
                package_path
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                for line in iter(lambda: process.stdout.readline(), ""):
                    if not line:
                        break
                    line = unicode(line.rstrip(), "utf-8")
                    if verbose:
                        click.echo(line)
                    else:
                        if 'already installed' in line:
                            is_error = True
                            click.echo(click.style('The package is already installed.', fg='blue'))
                            break
                        if '_tmpRPMcache_' in line:
                            is_error = True
                            click.echo('{} {}'.format(
                                click.style('ERROR:', fg='red'), line.replace('(ERROR)', '').strip()), err=True)
                            break
                if not is_error and not verbose:
                    click.echo('{} {}'.format(click.style('Installed successfully:', fg='green'), file_name))


@group_psdk.command()
@click.option('-p', '--package', type=click.STRING, required=True)
@click.option('-v', '--verbose', is_flag=True)
def sdk_remove(package, verbose):
    """Remove package from target."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    if len(psdks.keys()) != 1:
        click.echo('Found the installed Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(psdks.keys())))

    # Query index
    r_index = prompt_index(psdks.keys())
    key = list(psdks.keys())[r_index - 1]

    # Chroot
    chroot = psdks[key]

    # Check and query root permission
    check_sudoers_chroot(key)

    # Get psdk targets
    targets = get_list_targets(chroot)

    if not targets:
        click.echo('Targets in Aurora Platform SDK not found.')
        return

    if len(targets) != 1:
        click.echo('Found targets Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(targets)))

    # Query index
    r_index = prompt_index(targets)
    target = list(targets)[r_index - 1]

    # Has error
    is_error = False

    # Run execute
    with subprocess.Popen([
        chroot,
        'sb2',
        '-t',
        target,
        '-m',
        'sdk-install',
        '-R',
        'zypper',
        'rm',
        '-y',
        package
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        for line in iter(lambda: process.stdout.readline(), ""):
            if not line:
                break
            line = unicode(line.rstrip(), "utf-8")
            if verbose:
                click.echo(line)
            else:
                if 'Nothing to do' in line:
                    is_error = True
                    click.echo(click.style('The package not found.', fg='blue'))
                    break
        if not is_error and not verbose:
            click.echo('{} {}'.format(click.style('Remove successfully:', fg='green'), package))


@group_psdk.command()
def list_targets():
    """Get list targets."""

    psdks = get_list_psdk_installed()

    if not psdks:
        click.echo('Aurora Platform SDK not found.')
        return

    if len(psdks.keys()) != 1:
        click.echo('Found the installed Aurora Platform SDK:\n{}'
                   .format(get_string_from_list_numbered(psdks.keys())))

    # Query index
    r_index = prompt_index(psdks.keys())
    key = list(psdks.keys())[r_index - 1]

    # Chroot
    chroot = psdks[key]

    # Check and query root permission
    check_sudoers_chroot(key)

    # Get psdk targets
    targets = get_list_targets(chroot)

    if not targets:
        click.echo('Targets in Aurora Platform SDK not found.')
        return

    click.echo('Found targets Aurora Platform SDK:\n{}'
               .format(get_string_from_list(targets)))
