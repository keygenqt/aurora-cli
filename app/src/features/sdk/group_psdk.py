import os
import pathlib
import subprocess
from pathlib import Path

import click

from app.src.features.sdk.impl.download import multi_download
from app.src.features.sdk.impl.urls import get_map_versions, TypeSDK, get_urls_on_html
from app.src.features.sdk.impl.utils import get_string_from_list, get_string_from_list_numbered, prompt_index, \
    bar_subprocess_lines, bar_subprocess_symbol


@click.group(name='psdk')
def group_psdk():
    """Working with the Aurora Platform SDK."""
    pass


@group_psdk.command()
def available():
    """Get available version Aurora Platform SDK."""

    versions = get_map_versions(TypeSDK.PSDK)

    click.echo('Available Aurora Platform SDK versions:\n{}'
               .format(get_string_from_list(versions.keys())))


@group_psdk.command()
def install():
    """Download and run install Aurora Platform SDK."""

    versions = get_map_versions(TypeSDK.PSDK)

    click.echo('Select index Aurora Platform SDK versions:\n{}\n'
               .format(get_string_from_list_numbered(versions.keys())))

    index = prompt_index(versions.keys())
    key = list(versions.keys())[index - 1]
    url = '{}{}'.format(versions[key], key)

    links = get_urls_on_html(url)
    files = [item for item in links if 'md5sum' not in item]
    files_url = ['{}{}'.format(url, item) for item in files]

    files = multi_download(files_url)

    archive_chroot = [item for item in files if 'Chroot' in item and 'tar.bz2' in item]
    archive_tooling = [item for item in files if 'Tooling' in item]
    archive_target = [item for item in files if 'Target' in item]

    if not archive_chroot:
        click.echo('Chroot tar.bz2 not found.', err=True)
        return

    if not archive_tooling:
        click.echo('Tooling tar.bz2 not found.', err=True)
        return

    version = os.path.basename(archive_chroot[0]).split('-')[1]

    path_psdk = str(Path.home() / 'Aurora_Platform_SDK_{}'.format(version))
    path_chroot = '{}/sdks/aurora_psdk'.format(path_psdk)

    chroot = '{}/sdk-chroot'.format(path_chroot)

    if os.path.isdir(path_psdk):
        click.echo('\nError: Folder already exists: {}'.format(path_psdk), err=True)
        return

    pathlib.Path(path_psdk).mkdir()
    pathlib.Path(path_chroot).mkdir(parents=True, exist_ok=True)

    pathlib.Path('{}/toolings'.format(path_psdk)).mkdir()
    pathlib.Path('{}/tarballs'.format(path_psdk)).mkdir()
    pathlib.Path('{}/targets'.format(path_psdk)).mkdir()

    # Query sudo
    click.echo('')
    subprocess.call([
        'sudo',
        'echo',
        'Install chroot'
    ])

    # Install chroot with progress
    with subprocess.Popen([
        'sudo',
        'tar',
        '--numeric-owner',
        '-p',
        '-xjf',
        archive_chroot[0],
        '--blocking-factor=20',
        '--record-size=512',
        '--checkpoint=.10',
        '-C',
        path_chroot
    ], stdout=subprocess.PIPE) as process:
        # Ref size - 273205534 (bytes) == 175726 (checkpoint)
        archive_size = os.stat(archive_chroot[0]).st_size
        bar_subprocess_symbol(int(175726 * archive_size / 273205534), process)

    # Install tooling with progress
    click.echo('Install tooling')
    with subprocess.Popen([
        'sudo',
        chroot,
        'sdk-assistant',
        'tooling',
        'create',
        '-y',
        'AuroraOS-{}-base'.format(version),
        archive_tooling[0]
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        # Ref size - 10 output lines
        bar_subprocess_lines(10, process)

    # Install targets with progress
    for target in archive_target:
        arch = target.split('-')[-1].split('.')[0]
        click.echo('Install target "{}"'.format(arch))
        with subprocess.Popen([
            'sudo',
            chroot,
            'sdk-assistant',
            'target',
            'create',
            '-y',
            'AuroraOS-{}-base-{}'.format(version, arch),
            archive_tooling[0]
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
            # Ref size - 25 output lines
            bar_subprocess_lines(25, process)

    click.echo("""
{successfully}
    
You should update your ~/.bashrc to include export:

    {psdk_dir}

Add alias for convenience:

    {psdk_alias}

After that run the command:

    {source}

You can check the installation with the command:

    {list}
    
Good luck!""".format(
        successfully=click.style(
            'Install Aurora Platform "{}" SDK successfully!'.format(version),
            fg='green'
        ),
        psdk_dir=click.style(
            'export PSDK_DIR=$HOME/Aurora_Platform_SDK_{}/sdks/aurora_psdk'.format(version),
            fg='blue'
        ),
        psdk_alias=click.style(
            'alias aurora_psdk=$HOME/Aurora_Platform_SDK_{}/sdks/aurora_psdk/sdk-chroot'.format(version),
            fg='blue'
        ),
        source=click.style(
            'source $HOME/.bashrc',
            fg='blue'
        ),
        list=click.style(
            'aurora_psdk sdk-assistant list',
            fg='blue'
        ),
    ))
