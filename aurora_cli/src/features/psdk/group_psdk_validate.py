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
from aurora_cli.src.support.output import echo_stdout, echo_stderr, echo_line
from aurora_cli.src.support.texts import AppTexts


@click.group(name='validate', invoke_without_command=True)
@click.pass_context
@click.option('-p', '--path', multiple=True, type=click.STRING, required=True, help='Path to RPM file')
@click.option('-pr', '--profile', default='regular', type=click.Choice([
    'regular',
    'extended',
    'mdm',
    'antivirus',
    'auth',
], case_sensitive=False), help='Select profile')
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def psdk_validate(ctx: {}, path: [], profile, verbose: bool):
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
            '-p',
            profile,
            str(path)
        ], ctx.obj.get_type_output(verbose), ['.+ERROR.+'])
