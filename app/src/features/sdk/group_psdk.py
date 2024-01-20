import os
import pathlib
import subprocess
from pathlib import Path

import click

from app.src.features.sdk.impl.download import multi_download
from app.src.features.sdk.impl.urls import get_map_versions, TypeSDK, get_urls_on_html
from app.src.features.sdk.impl.utils import get_string_from_list, get_string_from_list_numbered, prompt_index


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
    psdk_path = str(Path.home() / 'Aurora_Platform_SDK_{}'.format(version))
    chroot_path = '{}/sdks/aurora_psdk'.format(psdk_path)
    chroot = '{}/sdk-chroot'.format(chroot_path)

    if os.path.isdir(psdk_path):
        click.echo('\nError: Folder already exists: {}'.format(psdk_path), err=True)
        return

    pathlib.Path(psdk_path).mkdir()
    pathlib.Path(chroot_path).mkdir(parents=True, exist_ok=True)

    pathlib.Path('{}/toolings'.format(psdk_path)).mkdir()
    pathlib.Path('{}/tarballs'.format(psdk_path)).mkdir()
    pathlib.Path('{}/targets'.format(psdk_path)).mkdir()

    click.echo('\nInstall chroot.')
    subprocess.call([
        'sudo',
        'tar',
        '--numeric-owner',
        '-p',
        '-xjf',
        archive_chroot[0],
        '--checkpoint=.1000',
        '-C',
        chroot_path
    ])

    click.echo('\nInstall tooling.')

    subprocess.call([
        chroot,
        'sdk-assistant',
        'tooling',
        'create',
        '-y',
        'AuroraOS-{}-base'.format(version),
        archive_tooling[0]
    ])

    for target in archive_target:
        arch = target.split('-')[-1].split('.')[0]
        click.echo('\nInstall target "{}".'.format(arch))
        subprocess.call([
            chroot,
            'sdk-assistant',
            'target',
            'create',
            '-y',
            'AuroraOS-{}-base-{}'.format(version, arch),
            archive_tooling[0]
        ])
