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
    get_psdk_chroot, check_sudoers_chroot, get_psdk_targets
from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.texts import AppTexts


@click.group(name='list-targets', invoke_without_command=True)
def psdk_list_targets():
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
