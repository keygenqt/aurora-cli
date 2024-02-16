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

from aurora_cli.src.features.psdk.impl.utils import clear_sudoers_psdk, psdk_folder_select, \
    add_sudoers_psdk, check_sdk_chroot
from aurora_cli.src.support.helper import sudo_request
from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.texts import AppTexts


@click.group(name='sudoers', invoke_without_command=True)
@click.option('-d', '--delete', is_flag=True, default=False, required=True, help="Enable remove sudoers permissions.")
def psdk_sudoers(delete: bool):
    """Update sudoers permissions Aurora Platform SDK."""

    folder = psdk_folder_select()

    if delete:
        # Check exist sudoers
        if not check_sdk_chroot(folder):
            echo_stdout(AppTexts.psdk_sudoers_not_exist_error())
            exit(0)
        # Get root permissions
        sudo_request()
        # Clear sudoers
        clear_sudoers_psdk(folder)
        # Output
        echo_stdout(AppTexts.psdk_clear_sudoers_success(folder.name))
    else:
        # Check not exist sudoers
        if check_sdk_chroot(folder):
            echo_stdout(AppTexts.psdk_sudoers_exist_error())
            exit(0)
        # Get root permissions
        sudo_request()
        # Add sudoers
        add_sudoers_psdk(folder)
        # Output
        echo_stdout(AppTexts.psdk_added_sudoers_success(folder.name))
