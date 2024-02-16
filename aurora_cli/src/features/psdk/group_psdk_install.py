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
from pathlib import Path

import click

from aurora_cli.src.features.psdk.impl.utils import get_url_psdk_archives, get_psdk_folder
from aurora_cli.src.support.alive_bar.progress_alive_bar import ProgressAliveBar
from aurora_cli.src.support.download import multi_download
from aurora_cli.src.support.helper import prompt_index, pc_command, sudo_request, \
    check_size_file, get_file_size
from aurora_cli.src.support.output import echo_stdout, echo_stderr, VerboseType, echo_line
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.versions import get_versions_sdk


@click.group(name='install', invoke_without_command=True)
@click.option('-l', '--latest', is_flag=True, help="Select latest version")
def psdk_install(latest: bool):
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

    # Check files size
    is_error_size = False
    for index, url in enumerate(archives):
        if not check_size_file(get_file_size(url), Path(files[index])):
            if not is_error_size:
                echo_line()
            echo_stderr(AppTexts.file_error_size(files[index]))
            is_error_size = True

    if is_error_size:
        echo_line()
        echo_stderr(AppTexts.file_error_size_common())
        exit(1)

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
