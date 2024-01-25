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
