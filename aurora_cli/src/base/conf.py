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
import pathlib
from pathlib import Path

import click.exceptions
import requests
from yaml import Loader
from yaml import load

from aurora_cli.src.base.helper import get_default_config
from aurora_cli.src.base.utils import get_full_path

# Default path config
PATH_CONF = '~/.aurora-cli/configuration.yaml'

# Public key pairs
URL_KEY = 'https://developer.auroraos.ru/static/regular_key.pem'
URL_CERT = 'https://developer.auroraos.ru/static/regular_cert.pem'


# Loader configuration yaml
class Conf:
    def __init__(self, path):

        self.conf_path = get_full_path(PATH_CONF)

        # Get path config
        if path is not None and os.path.isfile(path) and path.lower().endswith('.yaml'):
            self.conf_path = Path(path)
        else:
            if not os.path.isfile(self.conf_path):
                click.echo('{} {}'.format(click.style('Configuration file not found:', fg='red'), self.conf_path))
                self._create_default_config()

        # Check and download key pairs
        self._check_key_pairs()

        # Load config
        with open(self.conf_path, 'rb') as file:
            self.conf = load(file.read(), Loader=Loader)

    # Create default file configuration
    def _create_default_config(self):
        if not click.confirm('\nCreate default configuration file?'):
            exit(0)

        path_dir = os.path.dirname(self.conf_path)

        # Create dir if not exist
        if not os.path.isdir(path_dir):
            pathlib.Path(path_dir).mkdir()

        # Write default configuration file
        with open(self.conf_path, 'w') as file:
            print(get_default_config(), file=file)

        click.echo('\n{} {}\n'.format(
            click.style('Configuration file created successfully:', fg='green'), self.conf_path))

    # Check and download key pairs
    def _check_key_pairs(self):
        path_dir = Path(os.path.dirname(self.conf_path)) / 'keys'
        if not path_dir.is_dir():
            # Create a folder immediately to ask 1 time
            path_dir.mkdir()
            if click.confirm('Public key pairs not found, download them for you?'):
                click.echo('\nOne second...')
                # Names file
                key_name = os.path.basename(URL_KEY)
                cert_name = os.path.basename(URL_CERT)
                # Download
                key = requests.get(URL_KEY, allow_redirects=True)
                cert = requests.get(URL_CERT, allow_redirects=True)
                # Write
                with open(path_dir / key_name, 'wb') as file:
                    file.write(key.content)
                with open(path_dir / cert_name, 'wb') as file:
                    file.write(cert.content)

                click.echo(click.style('Public key pairs download successfully.\n', fg='green'))

    # Get debug path configuration
    @staticmethod
    def _get_path_debug():
        return Path(os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.realpath(__file__)))))) / "configuration.yaml"

    # Get config path
    def get_path(self):
        return self.conf_path

    # Get config keys
    def get_keys(self):
        keys = {}
        # If empty
        if not self.conf['keys']:
            return keys
        # Format keys
        for item in self.conf['keys']:
            # Check data
            if not item['name'] or not item['key'] or not item['cert']:
                click.echo('{} {}'.format(
                    click.style('The configuration file is filled in incorrectly:', fg='red'), self.conf_path))
                exit(1)
            keys[str(item['name'])] = {'key': str(item['key']), 'cert': str(item['cert'])}
        return keys

    # Get config devices
    def get_devices(self):
        devices = {}
        # If empty
        if not self.conf['devices']:
            return devices
        # Format keys
        for item in self.conf['devices']:
            # Check data
            if not item['ip'] or not item['pass'] or not item['port'] or not item['devel-su']:
                click.echo('{} {}'.format(
                    click.style('The configuration file is filled in incorrectly:', fg='red'), self.conf_path))
                exit(1)
            devices[str(item['ip'])] = {
                'pass': str(item['pass']), 'port': str(item['port']), 'devel-su': str(item['devel-su'])}
        return devices
