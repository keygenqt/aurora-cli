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
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from aurora_cli.src.support.helper import check_string_regex, get_request

# Url Aurora SDK
URL_AURORA_REPO_VERSION = 'https://sdk-repo.omprussia.ru/sdk/installers/{}/AppSDK/'


# Get installed sdk folder
def get_sdk_folder(workdir: Path):
    folders = [folder for folder in os.listdir(workdir) if
               os.path.isdir(workdir / folder) and 'Aurora' in folder and os.path.isfile(
                   workdir / folder / 'sdk-release')]
    if folders:
        return workdir / folders[0]
    return None


# Get installed Aurora SDK version
def get_sdk_installed_version(workdir: Path):
    folder = get_sdk_folder(workdir)
    if folder:
        with open(workdir / folder / 'sdk-release') as f:
            return f.readline().strip().split('=')[1].replace('-base', '')


# Find file sdk from version
def get_url_sdk_folder(version: str):
    versions = []
    url = URL_AURORA_REPO_VERSION.format(version)
    response = get_request(url)
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


# Find installer sdk from version
def get_url_sdk_run(version: str, install_type: str):
    url_folder = get_url_sdk_folder(version)
    response = get_request(url_folder)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text
            if check_string_regex(text, [r'^AuroraSDK.+linux.+{}.+\d\.run'.format(install_type)]):
                return '{}/{}'.format(url_folder, text)
    return None
