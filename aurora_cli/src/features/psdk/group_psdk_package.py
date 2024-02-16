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

from aurora_cli.src.features.psdk.impl.utils import psdk_folder_select, \
    get_psdk_chroot, check_sudoers_chroot, psdk_target_select
from aurora_cli.src.support.helper import pc_command, get_path_files
from aurora_cli.src.support.output import echo_stdout, echo_stderr, VerboseType, echo_line
from aurora_cli.src.support.texts import AppTexts


@click.group(name='package-install', invoke_without_command=True)
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def psdk_package_install(ctx: {}, path: [], verbose: bool):
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
        ], ctx.obj.get_type_output(verbose), ['^Nothing.+', '.+_tmpRPMcache_.+'])


@click.group(name='package-remove', invoke_without_command=True)
@click.pass_context
@click.option('-p', '--package', multiple=True, type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def psdk_package_remove(ctx: {}, package: [], verbose: bool):
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
        ], ctx.obj.get_type_output(verbose), ['^Nothing.+'])


@click.group(name='package-search', invoke_without_command=True)
@click.option('-p', '--package', multiple=True, type=click.STRING, required=True, help='Package name')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def psdk_package_search(package: [], verbose: bool):
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
        ], VerboseType.verbose if verbose else VerboseType.none, [], callback=output)
