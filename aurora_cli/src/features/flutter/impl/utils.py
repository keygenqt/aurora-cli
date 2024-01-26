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

import click
import requests


# Get list versions flutter
def get_versions_flutter():
    click.echo('Searching for versions on the server...')
    response = requests.get('https://gitlab.com/api/v4/projects/53055476/repository/tags?per_page=50')
    return [obj['name'] for obj in response.json()]


# Get list installed flutter
def get_list_flutter_installed():
    results = {}
    path = Path.home() / '.local' / 'opt'
    folders = [folder for folder in os.listdir(path) if os.path.isdir(path / folder)
               and 'flutter-' in folder
               and os.path.isfile(path / folder / 'bin' / 'flutter')]
    folders.sort(reverse=True)
    for folder in folders:
        key = folder.replace('flutter-', '')
        results[key] = str(path / folder)
    return results
