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
import requests
from bs4 import BeautifulSoup

from aurora_cli.src.support.helper import check_string_regex, get_request
from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.texts import AppTexts

# Url Aurora SDK
URL_AURORA_REPO = 'https://sdk-repo.omprussia.ru/sdk/installers/'

# Url Flutter SDK
URL_FLUTTER_SDK = 'https://gitlab.com/api/v4/projects/53055476/repository/tags?per_page=100'

# Url Flutter Plugins
URL_FLUTTER_PLUGINS = 'https://gitlab.com/api/v4/projects/48571226/repository/tags?per_page=100'


# Get list versions Aurora SDK
def get_versions_sdk(show_all: bool = False) -> []:
    versions = []
    echo_stdout(AppTexts.loading_server())
    response = get_request(URL_AURORA_REPO)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.replace('/', '')
            if check_string_regex(text, [r'\d.\d.\d']):
                versions.append(text)
    versions.reverse()
    if show_all:
        return versions
    else:
        return versions[:4]


# Get list versions flutter
def get_versions_flutter() -> []:
    echo_stdout(AppTexts.loading_server())
    response = get_request(URL_FLUTTER_SDK)
    return [obj['name'] for obj in response.json()]


# Get list plugins tags flutter for Aurora OS
def get_flutter_plugins() -> []:
    echo_stdout(AppTexts.loading_server())
    response = get_request(URL_FLUTTER_PLUGINS)
    return [obj['name'] for obj in response.json()]
