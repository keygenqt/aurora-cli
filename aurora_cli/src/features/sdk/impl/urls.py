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
import re
from enum import Enum

import click
import requests

# Repository link to SDK
REPO = 'https://sdk-repo.omprussia.ru/sdk/installers/'


# Types sdk: Aurora SDK and Platform SDK
class TypeSDK(Enum):
    SDK = 'AppSDK'
    PSDK = 'PlatformSDK'


# Find links on html page
def get_urls_on_html(url, is_folder=False):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    links = list(reversed([item for item in re.findall(r'href=[\'"]?([^\'" >]+)', response.text) if '..' not in item]))
    if is_folder:
        return [link for link in links if '/' in link]
    else:
        return [link for link in links if '/' not in link and '-pu' not in link]


# Find versions sdk from links
def get_map_versions(sdk_type: TypeSDK):
    click.echo('Searching for versions on the server...')
    versions = {}
    urls = get_urls_on_html(REPO, True)

    for url in urls:
        level2 = get_urls_on_html(f"{REPO}{url}{sdk_type.value}/", True)
        if level2:
            for item in level2:
                versions[item] = f"{REPO}{url}{sdk_type.value}/"

    return versions
