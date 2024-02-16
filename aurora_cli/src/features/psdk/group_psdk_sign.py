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

from aurora_cli.src.features.psdk.impl.utils import get_psdk_installed_versions, psdk_folder_select, \
    get_psdk_chroot, check_sudoers_chroot
from aurora_cli.src.support.helper import prompt_index, pc_command, check_empty_with_exit, get_path_file, get_path_files
from aurora_cli.src.support.output import echo_stdout, echo_stderr, VerboseType, echo_line
from aurora_cli.src.support.texts import AppTexts


@click.group(name='sign', invoke_without_command=True)
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-i', '--index', type=click.INT, help='Specify index')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def psdk_sign(ctx: {}, path: [], index: int, verbose: bool):
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

    # Check verbose
    verbose = ctx.obj.get_type_output(verbose)

    for path in paths:
        echo_line(len(get_psdk_installed_versions()) - 1)
        if verbose != VerboseType.verbose:
            echo_stdout(AppTexts.psdk_sign(path))
        # Remove if exist sign
        pc_command([
            str(chroot),
            'rpmsign-external',
            'delete',
            str(path)
        ], VerboseType.none)
        # Add sign
        pc_command([
            str(chroot),
            'rpmsign-external',
            'sign',
            '--key={}'.format(key_path),
            '--cert={}'.format(cert_path),
            str(path)
        ], verbose)
