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
import subprocess
from pathlib import Path

import click

from aurora_cli.src.features.psdk.impl.utils import clear_sudoers_psdk, psdk_folder_select
from aurora_cli.src.support.helper import clear_file_line
from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.texts import AppTexts


@click.group(name='remove', invoke_without_command=True)
def psdk_remove():
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
