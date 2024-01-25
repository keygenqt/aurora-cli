import os
import shutil
from pathlib import Path

import click
from git import Repo

from app.src.base.utils import get_string_from_list, get_string_from_list_numbered, prompt_index
from app.src.features.flutter.impl.git_progress_alive_bar import GitProgressAliveBar
from app.src.features.flutter.impl.utils import get_versions_flutter, get_list_flutter_installed


@click.group(name='flutter')
def group_flutter():
    """Working with the Flutter SDK for Aurora OS."""
    pass


@group_flutter.command()
def available():
    """Get available versions Flutter SDK."""

    versions = get_versions_flutter()

    click.echo('Available versions Flutter SDK:\n{}'
               .format(get_string_from_list(versions)))


@group_flutter.command()
@click.option('-l', '--latest', is_flag=True, help="Latest tag")
def install(latest):
    """Install Flutter SDK for Aurora OS."""

    versions = get_versions_flutter()

    if not latest:
        click.echo('Select index Flutter SDK versions:\n{}'
                   .format(get_string_from_list_numbered(versions)))
        index = prompt_index(versions)
        tag = list(versions)[index - 1]
    else:
        tag = list(versions)[0]

    flutter_root_path = Path.home() / '.local' / 'opt'
    clone_path = str(flutter_root_path / 'flutter-{}'.format(tag))

    if os.path.isdir(clone_path):
        click.echo(click.style('\nError: Folder already exists: {}'.format(clone_path), fg='red'), err=True)
        exit(1)

    # noinspection PyTypeChecker
    repo = Repo.clone_from(
        url='https://gitlab.com/omprussia/flutter/flutter.git',
        to_path=clone_path,
        progress=GitProgressAliveBar()
    )

    # Checkout to tag
    repo.git.checkout(tag)

    click.echo("""
{successfully}

Add alias to ~/.bashrc for convenience:

    {flutter_alias}

After that run the command:

    {source}

You can check the installation with the command:

    {version}

Good luck!""".format(
        successfully=click.style(
            'Install Flutter SDK "{}" successfully!'.format(tag),
            fg='green'
        ),
        flutter_alias=click.style(
            'alias flutter-aurora=$HOME/.local/opt/flutter-{}/bin/flutter'.format(tag),
            fg='blue'
        ),
        source=click.style(
            'source $HOME/.bashrc',
            fg='blue'
        ),
        version=click.style(
            'flutter-aurora --version',
            fg='blue'
        ),
    ))


@group_flutter.command()
def installed():
    """Get installed list Flutter SDK."""

    flutters = get_list_flutter_installed()

    if not flutters:
        click.echo('Flutter SDK not found.')
        return

    click.echo('Found the installed Flutter SDK:\n{}'
               .format(get_string_from_list(flutters.keys())))


@group_flutter.command()
def remove():
    """Remove Flutter SDK."""

    flutters = get_list_flutter_installed()

    if not flutters:
        click.echo('Flutter SDK not found.')
        return

    if len(flutters.keys()) != 1:
        click.echo('Found the installed Flutter SDK:\n{}'
                   .format(get_string_from_list_numbered(flutters.keys())))

    # Query index
    index = prompt_index(flutters.keys())
    key = list(flutters.keys())[index - 1]
    path = flutters[key]

    # Remove folder
    shutil.rmtree(path)

    # Clear .bashrc
    with open(Path.home() / '.bashrc', 'r') as f:
        lines = f.readlines()
    with open(Path.home() / '.bashrc', 'w') as f:
        for line in lines:
            if path.replace(str(Path.home()), '') not in line:
                f.write(line)

    click.echo(click.style(
        'Remove Flutter SDK successfully!',
        fg='green'
    ))
