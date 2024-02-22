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

from aurora_cli.src.features.psdk.impl.utils import psdk_folder_select, get_psdk_chroot, check_sudoers_chroot, \
    get_psdk_targets
from aurora_cli.src.support.helper import pc_command
from aurora_cli.src.support.output import echo_stdout, echo_line, VerboseType
from aurora_cli.src.support.texts import AppTexts


@click.group(name='clear', invoke_without_command=True)
@click.pass_context
@click.option('-v', '--verbose', is_flag=True, help='Detailed output')
def psdk_clear(ctx: {}, verbose: bool):
    """Remove snapshots targets."""

    workdir = ctx.obj.get_workdir()
    folder = psdk_folder_select(workdir)

    # Chroot
    chroot = get_psdk_chroot(folder)

    # Check permission
    check_sudoers_chroot(folder)

    # Targets
    targets = get_psdk_targets(chroot)

    if not targets:
        echo_stdout(AppTexts.psdk_installed_targets_not_found())
        exit(1)

    # Check verbose
    verbose = ctx.obj.get_type_output(verbose)

    for i, target in enumerate(targets):
        if i != 0:
            echo_line()
        if verbose != VerboseType.verbose:
            echo_stdout(AppTexts.psdk_remove_snapshot(target))
        # Add sign
        pc_command([
            str(chroot),
            'sdk-assistant',
            'target',
            'remove',
            '-y',
            '--snapshots-of',
            target
        ], verbose)
