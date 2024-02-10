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
import subprocess
from pathlib import Path

import click

from aurora_cli.src.features.psdk.impl.utils import get_psdk_installed_versions, get_url_psdk_archives, get_psdk_folder, \
    clear_sudoers_psdk, psdk_folder_select, add_sudoers_psdk, get_psdk_chroot, check_sudoers_chroot, psdk_target_select, \
    get_psdk_targets
from aurora_cli.src.support.alive_bar.progress_alive_bar import ProgressAliveBar
from aurora_cli.src.support.download import multi_download
from aurora_cli.src.support.helper import prompt_index, pc_command, clear_file_line, sudo_request, \
    check_empty_with_exit, get_path_file, get_path_files
from aurora_cli.src.support.output import echo_stdout, echo_stderr, VerboseType, echo_line
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.versions import get_versions_sdk


@click.group(name='psdk')
def group_psdk():
    """Working with the Aurora Platform SDK."""
    pass


@group_psdk.command()
def available():
    """Get available version Aurora Platform SDK."""

    versions = get_versions_sdk()

    echo_stdout(AppTexts.psdk_versions(versions))


@group_psdk.command()
@click.option('-l', '--latest', is_flag=True, help="Select latest version")
def install(latest: bool):
    """Download and install Aurora Platform SDK."""

    versions = get_versions_sdk()

    echo_stdout(AppTexts.select_versions(versions))
    echo_stdout(AppTexts.array_indexes(versions), 2)

    # Query index
    index = prompt_index(versions, 1 if latest else None)

    # Select tag
    version = versions[index]

    # Get links
    archives = get_url_psdk_archives(version)

    # Check is not empty
    if not archives:
        echo_stderr(AppTexts.sdk_not_found())

    # Download if needed
    files = multi_download(archives)

    # Find archive
    archive_chroot = [item for item in files if 'Chroot' in item and 'tar.bz2' in item]
    archive_tooling = [item for item in files if 'Tooling' in item]
    archive_target = [item for item in files if 'Target' in item]

    # Check exist chroot
    if not archive_chroot:
        echo_stderr(AppTexts.psdk_not_found_chroot())
        exit(1)

    # Check exist tooling
    if not archive_tooling:
        echo_stderr(AppTexts.psdk_not_found_tooling())
        exit(1)

    # Update to full version
    version = archive_chroot[0].split('-')[1]

    # Get path for install
    path_psdk = get_psdk_folder(version)
    path_chroot = '{}/sdks/aurora_psdk'.format(path_psdk)

    # Chroot path
    chroot = '{}/sdk-chroot'.format(path_chroot)

    # Check psdk already folder exist
    if path_psdk.is_dir():
        echo_line()
        echo_stderr(AppTexts.dir_already_exist(str(path_psdk)))
        exit(1)

    # Get root permissions
    sudo_request()

    # Create folders
    Path(path_psdk).mkdir()
    Path(path_chroot).mkdir(parents=True, exist_ok=True)
    Path('{}/toolings'.format(path_psdk)).mkdir()
    Path('{}/tarballs'.format(path_psdk)).mkdir()
    Path('{}/targets'.format(path_psdk)).mkdir()

    # Create ssh bar
    bar = ProgressAliveBar()
    # Ref size - 273205534 (bytes) == 175726 (checkpoint)
    archive_size = os.stat(archive_chroot[0]).st_size
    total = int(175726 * archive_size / 273205534) + 10

    echo_stdout(AppTexts.psdk_start_install_chroot())
    pc_command([
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
    ], VerboseType.none, [], callback=lambda _, i: bar.update(i, total), is_char=True)
    bar.update(total, total)

    # Create ssh bar
    bar = ProgressAliveBar()
    # Ref size - 20 output lines
    total = 20

    echo_stdout(AppTexts.psdk_start_install_tooling())
    pc_command([
        chroot,
        'sdk-assistant',
        'tooling',
        'create',
        '-y',
        'AuroraOS-{}-base'.format(version),
        archive_tooling[0]
    ], VerboseType.none, [], callback=lambda _, i: bar.update(i, total))
    bar.update(20, total)

    for target in archive_target:
        # Create ssh bar
        bar = ProgressAliveBar()
        # Ref size - 30 output lines
        total = 30
        arch = target.split('-')[-1].split('.')[0]
        echo_stdout(AppTexts.psdk_start_install_target(arch))
        pc_command([
            chroot,
            'sdk-assistant',
            'target',
            'create',
            '-y',
            'AuroraOS-{}-base-{}'.format(version, arch),
            target
        ], VerboseType.none, [], callback=lambda _, i: bar.update(i, total))
        bar.update(30, total)

    echo_stdout(AppTexts.psdk_install_success(version))


@group_psdk.command()
def installed():
    """Get installed list Aurora Platform SDK."""

    versions = get_psdk_installed_versions()

    if versions:
        echo_stdout(AppTexts.psdk_installed_versions(versions))
    else:
        echo_stderr(AppTexts.psdk_not_found())


@group_psdk.command()
def remove():
    """Remove installed Aurora Platform SDK."""

    folder = psdk_folder_select()

    if not click.confirm(AppTexts.psdk_remove_confirm(str(folder))):
        exit(0)

    echo_stdout(AppTexts.loading())

    # Remove folder psdk
    subprocess.call([
        'sudo',
        'rm',
        '-rf',
        str(folder)
    ])

    # Clear .bashrc
    clear_file_line(Path.home() / '.bashrc', folder.name)

    # Clear sudoers
    clear_sudoers_psdk(folder)

    # Output
    echo_stdout(AppTexts.psdk_remove_success())


@group_psdk.command()
@click.option('-d', '--delete', is_flag=True, default=False, required=True, help="Enable remove sudoers permissions.")
def sudoers(delete):
    """Update sudoers permissions Aurora Platform SDK."""

    folder = psdk_folder_select()

    # Get root permissions
    sudo_request()

    if delete:
        # Clear sudoers
        clear_sudoers_psdk(folder)
        # Output
        echo_stdout(AppTexts.psdk_clear_sudoers_success(folder.name))
    else:
        # Add sudoers
        add_sudoers_psdk(folder)
        # Output
        echo_stdout(AppTexts.psdk_added_sudoers_success(folder.name))


@group_psdk.command()
def list_targets():
    """Get list targets."""

    folder = psdk_folder_select()

    # Chroot
    chroot = get_psdk_chroot(folder)

    # Check permission
    check_sudoers_chroot(folder)

    # Targets
    targets = get_psdk_targets(chroot)

    if targets:
        echo_stdout(AppTexts.psdk_targets_list(targets))
    else:
        echo_stdout(AppTexts.psdk_installed_targets_not_found())


@group_psdk.command()
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def sign(ctx: {}, path: [], index: int, verbose: bool):
    """Sign (with re-sign) RPM package."""

    folder = psdk_folder_select()

    # Chroot
    chroot = get_psdk_chroot(folder)

    # Check permission
    check_sudoers_chroot(folder)

    # Keys list
    keys = check_empty_with_exit(ctx.obj.get_keys(), AppTexts.psdk_sign_keys_not_found())

    echo_stdout(AppTexts.select_keys(keys.keys()))
    echo_stdout(AppTexts.array_indexes(keys.keys()), 2)

    # Query index
    index = prompt_index(keys.keys(), index)
    key = list(keys.keys())[index]

    key_path = get_path_file(keys[key]['key'])
    cert_path = get_path_file(keys[key]['cert'])

    if not os.path.isfile(key_path) or not os.path.isfile(cert_path):
        echo_stderr(AppTexts.psdk_sign_keys_not_found())
        exit(1)

    # Read paths
    paths = get_path_files(path, extension='rpm')

    if not paths:
        echo_stderr(AppTexts.file_no_one_not_found())
        exit(1)

    for path in paths:
        echo_line()
        echo_stdout(AppTexts.psdk_sign(path))
        # Remove if exist sign
        pc_command([
            str(chroot),
            'rpmsign-external',
            'delete',
            str(path)
        ], VerboseType.true if verbose else VerboseType.none)
        # Add sign
        pc_command([
            str(chroot),
            'rpmsign-external',
            'sign',
            '--key={}'.format(key_path),
            '--cert={}'.format(cert_path),
            str(path)
        ], VerboseType.true if verbose else VerboseType.false)


@group_psdk.command()
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def validate(path: [], verbose: bool):
    """Validate RPM packages."""

    folder = psdk_folder_select()

    # Chroot
    chroot = get_psdk_chroot(folder)

    # Check permission
    check_sudoers_chroot(folder)

    # Target select
    target = psdk_target_select(chroot)

    # Read paths
    paths = get_path_files(path, extension='rpm')

    if not paths:
        echo_stderr(AppTexts.file_no_one_not_found())
        exit(1)

    for path in paths:
        echo_line()
        echo_stdout(AppTexts.psdk_validate(path))
        pc_command([
            str(chroot),
            'sb2',
            '-t',
            target,
            '-m',
            'emulate',
            'rpm-validator',
            str(path)
        ], VerboseType.true if verbose else VerboseType.false, ['.+ERROR.+'])


@group_psdk.command()
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def package_install(path: [], verbose: bool):
    """Install RPM packages to target."""

    folder = psdk_folder_select()

    # Chroot
    chroot = get_psdk_chroot(folder)

    # Check permission
    check_sudoers_chroot(folder)

    # Target select
    target = psdk_target_select(chroot)

    # Read paths
    paths = get_path_files(path, extension='rpm')

    if not paths:
        echo_stderr(AppTexts.file_no_one_not_found())
        exit(1)

    for path in paths:
        echo_line()
        echo_stdout(AppTexts.psdk_target_package_install(path))
        pc_command([
            str(chroot),
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
            str(path)
        ], VerboseType.true if verbose else VerboseType.false, ['^Nothing.+', '.+_tmpRPMcache_.+'])


@group_psdk.command()
@click.option('-p', '--package', multiple=True, type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def package_remove(package: [], verbose: bool):
    """Remove RPM packages from target."""

    folder = psdk_folder_select()

    # Chroot
    chroot = get_psdk_chroot(folder)

    # Check permission
    check_sudoers_chroot(folder)

    # Target select
    target = psdk_target_select(chroot)

    for package_name in package:
        echo_line()
        echo_stdout(AppTexts.psdk_target_package_remove(package_name))
        pc_command([
            str(chroot),
            'sb2',
            '-t',
            target,
            '-m',
            'sdk-install',
            '-R',
            'zypper',
            'rm',
            '-y',
            package_name
        ], VerboseType.true if verbose else VerboseType.false, ['^Nothing.+'])


@group_psdk.command()
@click.option('-p', '--package', multiple=True, type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def package_search(package: [], verbose: bool):
    """Search installed RPM packages in target."""

    folder = psdk_folder_select()

    # Chroot
    chroot = get_psdk_chroot(folder)

    # Check permission
    check_sudoers_chroot(folder)

    # Target select
    target = psdk_target_select(chroot)

    def output(line, _):
        if not verbose and 'No matching items found' in line:
            echo_stdout(AppTexts.psdk_target_package_not_found())
        if not verbose and 'S  |' in line:
            echo_stdout(line)
        if not verbose and '---+' in line:
            echo_stdout(line)
        if not verbose and 'i+ |' in line:
            name = line.split('|')[1]
            echo_stdout(line.replace(name, click.style(name, fg='blue')))

    for package_name in package:
        echo_line()
        echo_stdout(AppTexts.psdk_target_package_search(package_name))
        # Remove if exist sign
        pc_command([
            str(chroot),
            'sb2',
            '-t',
            target,
            '-R',
            'zypper',
            'search',
            '--installed-only',
            '-s',
            package_name
        ], VerboseType.true if verbose else VerboseType.none, [], callback=output)
