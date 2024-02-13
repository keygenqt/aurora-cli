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
import getpass
import os
import subprocess
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from aurora_cli.src.support.helper import check_string_regex, clear_file_line, prompt_index, sudo_request, pc_command
from aurora_cli.src.support.output import echo_stdout, VerboseType
from aurora_cli.src.support.texts import AppTexts

# Url Aurora SDK
URL_AURORA_REPO_VERSION = 'https://sdk-repo.omprussia.ru/sdk/installers/{}/PlatformSDK/'

# Sudoers chroot mer-sdk-chroot
MER_SDK_CHROOT = '/etc/sudoers.d/mer-sdk-chroot'
MER_SDK_CHROOT_DATA = '''{username} ALL=(ALL) NOPASSWD: {folder_psdk}/sdks/aurora_psdk
Defaults!{folder_psdk}/sdks/aurora_psdk env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"
'''

# Sudoers chroot sdk-chroot
SDK_CHROOT = '/etc/sudoers.d/sdk-chroot'
SDK_CHROOT_DATA = '''{username} ALL=(ALL) NOPASSWD: {folder_psdk}/sdks/aurora_psdk/sdk-chroot
Defaults!{folder_psdk}/sdks/aurora_psdk/sdk-chroot env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"
'''


# Get installed psdk folder
def get_psdk_folders() -> []:
    result = []
    folders = [folder for folder in os.listdir(Path.home()) if
               os.path.isdir(Path.home() / folder) and 'Aurora_Platform_SDK_' in folder and os.path.isfile(
                   Path.home() / folder / 'sdks' / 'aurora_psdk' / 'etc' / 'os-release')]
    for folder in folders:
        result.append(Path.home() / folder)
    return result


# Get installed Aurora Platform SDK version
def get_psdk_installed_versions() -> []:
    result = []
    folders = get_psdk_folders()
    for folder in folders:
        with open(Path.home() / folder / 'sdks' / 'aurora_psdk' / 'etc' / 'os-release') as f:
            result.append([item for item in f.readlines() if 'VERSION_ID' in item][0].split('=')[1].strip())
    return result


# Find file sdk from version
def get_url_sdk_folder(version: str) -> str | None:
    versions = []
    url = URL_AURORA_REPO_VERSION.format(version)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.replace('/', '')
            if check_string_regex(text, [r'^\d.\d.\d']):
                versions.append(int(text.replace(version, '').replace('.', '')))

    if versions:
        versions.sort()
        return '{}{}.{}'.format(url, version, versions[-1])

    return None


# Find archive Platform SDK
def get_url_psdk_archives(version: str) -> []:
    url_folder = get_url_sdk_folder(version)
    response = requests.get(url_folder)
    result = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text
            if 'md5sum' not in text and 'Aurora_OS' in text and '-pu' not in text:
                result.append('{}/{}'.format(url_folder, text))
    return result


# Get path to folder psdk
def get_psdk_folder(version: str) -> Path:
    return Path.home() / 'Aurora_Platform_SDK_{}'.format(version)


# Get path to folder psdk
def get_psdk_chroot(folder: Path) -> Path:
    return folder / 'sdks' / 'aurora_psdk' / 'sdk-chroot'


# Update permissions sudoers
def update_permissions_sudoers_for_change(path: Path):
    if path.is_file():
        subprocess.call(['sudo', 'chmod', '777', path],
                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# Update permissions sudoers
def update_permissions_sudoers_for_use(path: Path):
    if path.is_file():
        subprocess.call(['sudo', 'chmod', '644', path],
                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.call(['sudo', 'chown', 'root:root', path],
                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


# Check sdk_chroot if exist - true
def check_sdk_chroot(folder: Path) -> bool:
    file = Path(SDK_CHROOT)
    with open(file, 'r') as file:
        for line in file:
            if folder.name in line:
                return True
    return False


# Add sudoers files psdk by folder name
def add_sudoers_psdk(folder: Path):
    # Add /etc/sudoers.d/mer-sdk-chroot
    mer_sdk_chroot = Path(MER_SDK_CHROOT)
    # Create file if not exist
    if not mer_sdk_chroot.is_file():
        subprocess.call(['sudo', 'touch', str(mer_sdk_chroot)])
    # Update permission for update file
    update_permissions_sudoers_for_change(mer_sdk_chroot)
    # Update file
    with open(mer_sdk_chroot, 'a') as file:
        file.write(MER_SDK_CHROOT_DATA.format(username=getpass.getuser(), folder_psdk=folder))
    # Change permission to root
    update_permissions_sudoers_for_use(mer_sdk_chroot)

    # Add /etc/sudoers.d/sdk-chroot
    sdk_chroot = Path(SDK_CHROOT)
    # Create file if not exist
    if not sdk_chroot.is_file():
        subprocess.call(['sudo', 'touch', str(sdk_chroot)])
    # Update permission for update file
    update_permissions_sudoers_for_change(sdk_chroot)
    # Update file
    with open(sdk_chroot, 'a') as file:
        file.write(SDK_CHROOT_DATA.format(username=getpass.getuser(), folder_psdk=folder))
    # Change permission to root
    update_permissions_sudoers_for_use(sdk_chroot)


# Clear sudoers files psdk by folder name
def clear_sudoers_psdk(folder: Path):
    # Clear /etc/sudoers.d/mer-sdk-chroot
    mer_sdk_chroot = Path(MER_SDK_CHROOT)
    update_permissions_sudoers_for_change(mer_sdk_chroot)
    clear_file_line(mer_sdk_chroot, folder.name)
    update_permissions_sudoers_for_use(mer_sdk_chroot)

    # Clear /etc/sudoers.d/sdk-chroot
    sdk_chroot = Path(SDK_CHROOT)
    update_permissions_sudoers_for_change(sdk_chroot)
    clear_file_line(sdk_chroot, folder.name)
    update_permissions_sudoers_for_use(sdk_chroot)


# Select psdk folder
def psdk_folder_select() -> Path:
    versions = get_psdk_installed_versions()

    if not versions:
        echo_stdout(AppTexts.psdk_installed_not_found())
        exit(1)

    echo_stdout(AppTexts.select_versions(versions))
    echo_stdout(AppTexts.array_indexes(versions), 2)

    # Query index
    index = prompt_index(versions)

    # Folder psdk
    folder = get_psdk_folder(versions[index])

    if not folder.is_dir():
        echo_stdout(AppTexts.psdk_folder_psdk_not_found(str(folder)))
        exit(1)

    return folder


# Get list psdk targets
def get_psdk_targets(chroot: Path) -> []:
    targets = []
    output = pc_command([
        str(chroot),
        'sdk-assistant',
        'list',
    ], VerboseType.none)

    for line in output:
        if '─' in line and 'default' not in line:
            targets.append(line[2:])

    return targets


# Get list psdk targets
def psdk_target_select(chroot: Path) -> []:
    targets = get_psdk_targets(chroot)

    if not targets:
        echo_stdout(AppTexts.psdk_installed_targets_not_found())
        exit(1)

    echo_stdout(AppTexts.select_target(targets))
    echo_stdout(AppTexts.array_indexes(targets), 2)

    # Query index
    index = prompt_index(targets)

    return targets[index]


# Check is add psdk sudoers and run sudo query
def check_sudoers_chroot(folder: Path):
    if os.path.isfile(SDK_CHROOT):
        with open(SDK_CHROOT) as f:
            if folder.name in f.read():
                return
    # Request sudo if not found sudoers chroot
    sudo_request()
