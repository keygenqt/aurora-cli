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

from aurora_cli.src.base.sdk import get_sdk_installed
from aurora_cli.src.base.utils import get_string_from_list, get_string_from_list_numbered, prompt_index
from aurora_cli.src.features.sdk.impl.download import multi_download
from aurora_cli.src.features.sdk.impl.urls import get_map_versions, TypeSDK, get_urls_on_html


@click.group(name='sdk')
def group_sdk():
    """Working with the Aurora SDK."""
    pass


@group_sdk.command()
def available():
    """Get available version Aurora SDK."""

    versions = get_map_versions(TypeSDK.SDK)

    click.echo('Available Aurora SDK versions:\n{}'
               .format(get_string_from_list(versions.keys())))


@group_sdk.command()
def installed():
    """Get version installed Aurora SDK."""

    version, _ = get_sdk_installed()

    if version:
        click.echo(version)
    else:
        click.echo('Aurora SDK not found.')


@group_sdk.command()
@click.option('-l', '--latest', is_flag=True, help="Select latest version")
@click.option('-t', '--install-type', default='offline', type=click.Choice(['offline', 'online'], case_sensitive=False))
def install(latest, install_type):
    """Download and run install Aurora SDK."""

    version, _ = get_sdk_installed()

    if version:
        click.echo(click.style('Aurora SDK already installed, only install one at a time.', fg='red'), err=True)
        exit(0)

    versions = get_map_versions(TypeSDK.SDK)

    if not latest:
        # Query index
        click.echo('Select index Aurora SDK versions:\n{}'
                   .format(get_string_from_list_numbered(versions.keys())))
        index = prompt_index(versions.keys())
        key = list(versions.keys())[index - 1]
    else:
        key = list(versions.keys())[0]

    url = '{}{}'.format(versions[key], key)

    links = get_urls_on_html(url)
    files = [item for item in links if 'run' in item and install_type in item]
    files_url = ['{}{}'.format(url, item) for item in files]

    files = multi_download(files_url)

    if files:
        os.chmod(files[0], os.stat(files[0]).st_mode | stat.S_IEXEC)
        cmds = shlex.split(files[0])
        subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        click.echo(click.style('Error: Something went wrong.', fg='red'), err=True)


@group_sdk.command()
def tool():
    """Run maintenance tool (remove, update)."""

    _, path = get_sdk_installed()

    if not path:
        click.echo('Aurora SDK not found.')
        return

    path = Path(path) / 'SDKMaintenanceTool'

    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
    cmds = shlex.split(str(path))
    subprocess.Popen(cmds, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)



