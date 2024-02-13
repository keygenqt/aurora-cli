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
import shlex
import stat
import subprocess
from pathlib import Path

import click

from aurora_cli.src.features.sdk.impl.utils import get_sdk_installed_version, get_sdk_folder, get_url_sdk_run
from aurora_cli.src.support.download import multi_download
from aurora_cli.src.support.helper import prompt_index, check_size_file, get_file_size
from aurora_cli.src.support.output import echo_stdout, echo_stderr, echo_line
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.versions import get_versions_sdk


@click.group(name='sdk')
def group_sdk():
    """Working with the Aurora SDK."""
    pass


@group_sdk.command()
def available():
    """Get available version Aurora SDK."""

    versions = get_versions_sdk()

    echo_stdout(AppTexts.sdk_versions(versions))


@group_sdk.command()
@click.option('-l', '--latest', is_flag=True, help='Select latest version')
@click.option('-t', '--install-type', default='offline', type=click.Choice(['offline', 'online'], case_sensitive=False),
              help='Select installer type')
def install(latest: bool, install_type: str):
    """Download and run install Aurora SDK."""

    version = get_sdk_installed_version()

    if version:
        echo_stderr(AppTexts.sdk_already_exist(version))
        exit(1)

    versions = get_versions_sdk()

    echo_stdout(AppTexts.select_versions(versions))
    echo_stdout(AppTexts.array_indexes(versions), 2)

    # Query index
    index = prompt_index(versions, 1 if latest else None)

    # Select tag
    version = versions[index]

    # Get url path
    installer_url = get_url_sdk_run(version, install_type)

    if not installer_url:
        echo_stderr(AppTexts.sdk_not_found())

    # Download file installer
    installer_path = multi_download([installer_url])[0]

    # Check file size
    if not check_size_file(get_file_size(installer_url), Path(installer_path)):
        echo_line()
        echo_stderr(AppTexts.file_error_size(installer_path))
        echo_stderr(AppTexts.file_error_size_common())
        exit(1)

    # Run installer
    os.chmod(installer_path, os.stat(installer_path).st_mode | stat.S_IEXEC)
    cmds = shlex.split(installer_path)
    subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@group_sdk.command()
def installed():
    """Get version installed Aurora SDK."""

    version = get_sdk_installed_version()

    if version:
        echo_stdout(AppTexts.sdk_version(version))
    else:
        echo_stderr(AppTexts.sdk_not_found())


@group_sdk.command()
def tool():
    """Run maintenance tool (remove, update)."""

    folder = get_sdk_folder()

    if not folder:
        echo_stderr(AppTexts.sdk_not_found())
        exit(1)

    path = Path(folder) / 'SDKMaintenanceTool'

    # Run maintenance tool
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
    cmds = shlex.split(str(path))
    subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
