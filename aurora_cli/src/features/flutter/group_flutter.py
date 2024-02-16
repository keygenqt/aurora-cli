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
import shutil
from pathlib import Path

import click
from git import Repo

from aurora_cli.src.features.flutter.group_flutter_build import group_flutter_build
from aurora_cli.src.features.flutter.group_flutter_debug import group_flutter_debug
from aurora_cli.src.features.flutter.impl.utils import get_list_flutter_installed
from aurora_cli.src.support.alive_bar.git_progress_alive_bar import GitProgressAliveBar
from aurora_cli.src.support.helper import prompt_index, clear_file_line
from aurora_cli.src.support.output import echo_stdout, echo_stderr
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.versions import get_versions_flutter


@click.group(name='flutter')
def group_flutter():
    """Working with the Flutter SDK for Aurora OS."""
    pass


# Add subgroup
group_flutter.add_command(group_flutter_debug)
group_flutter.add_command(group_flutter_build)


@group_flutter.command()
def available():
    """Get available versions Flutter SDK."""

    versions = get_versions_flutter()

    echo_stdout(AppTexts.flutter_versions(versions))


@group_flutter.command()
@click.option('-l', '--latest', is_flag=True, help="Select latest version")
def install(latest: bool):
    """Install Flutter SDK for Aurora OS."""

    versions = get_versions_flutter()

    echo_stdout(AppTexts.select_versions(versions))
    echo_stdout(AppTexts.array_indexes(versions), 2)

    # Query index
    index = prompt_index(versions, 1 if latest else None)

    # Select tag
    tag = versions[index]

    flutter_root_path = Path.home() / '.local' / 'opt'
    clone_path = str(flutter_root_path / 'flutter-{}'.format(tag))

    if os.path.isdir(clone_path):
        echo_stderr(AppTexts.dir_already_exist(clone_path))
        exit(1)

    # noinspection PyTypeChecker
    repo = Repo.clone_from(
        url='https://gitlab.com/omprussia/flutter/flutter.git',
        to_path=clone_path,
        progress=GitProgressAliveBar()
    )

    # Checkout to tag
    repo.git.checkout(tag)

    # Output
    echo_stdout(AppTexts.flutter_install_success(tag))


@group_flutter.command()
def installed():
    """Get installed list Flutter SDK."""

    versions = get_list_flutter_installed()

    if not versions:
        echo_stdout(AppTexts.flutter_installed_not_found())
        exit(1)

    echo_stdout(AppTexts.flutter_installed_versions(versions))


@group_flutter.command()
def remove():
    """Remove Flutter SDK."""

    versions = get_list_flutter_installed()

    if not versions:
        echo_stdout(AppTexts.flutter_installed_not_found())
        exit(1)

    echo_stdout(AppTexts.select_versions(versions))
    echo_stdout(AppTexts.array_indexes(versions), 2)

    # Query index
    index = prompt_index(versions)

    # Folder name
    folder = 'flutter-{}'.format(versions[index])

    # Path to flutter
    path = Path.home() / '.local' / 'opt' / folder

    if not click.confirm(AppTexts.flutter_remove_confirm(str(path))):
        exit(0)

    # Remove folder
    shutil.rmtree(path)

    # Clear .bashrc
    clear_file_line(Path.home() / '.bashrc', folder)

    # Output
    echo_stdout(AppTexts.flutter_remove_success())
