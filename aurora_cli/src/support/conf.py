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

import click.exceptions
import requests
from yaml import Loader
from yaml import load

from aurora_cli.src.support.helper import get_path_file
from aurora_cli.src.support.output import echo_stdout, VerboseType
from aurora_cli.src.support.texts import AppTexts

# Data versions
APP_NAME = 'aurora-cli'
APP_VERSION = '2.3.0'

# Default path config
PATH_CONF = '~/.aurora-cli/configuration.yaml'

# Temp folder
PATH_TEMP = '~/.aurora-cli/temp'

# Public key pairs
URL_KEY = 'https://developer.auroraos.ru/static/regular_key.pem'
URL_CERT = 'https://developer.auroraos.ru/static/regular_cert.pem'


# Loader configuration yaml
class Conf:

    @staticmethod
    def get_temp_folder() -> str:
        temp_folder = Path(get_path_file(PATH_TEMP, check_exist=False))
        if not temp_folder.is_dir():
            temp_folder.mkdir(parents=True, exist_ok=True)
        return str(temp_folder)

    @staticmethod
    def get_app_name() -> str:
        return APP_NAME

    @staticmethod
    def get_app_version() -> str:
        return APP_VERSION

    @staticmethod
    def _get_default_config() -> str:
        return """## Application configuration file Aurora CLI
## Version config: 0.0.2

## Type output: short | command | verbose
output: short

## Path to sign keys
## name - The name you will see in the list
## key  - Path to the key.pem file
## cert - Path to the cert.pem file
keys:
  - name: Public
    key: ~/.aurora-cli/keys/regular_key.pem
    cert: ~/.aurora-cli/keys/regular_cert.pem

## Devices list
## ip       - Device IP WI-FI or cable connection
## pass     - SSH password
## port     - SSH port
## devel-su - Device root password
devices:
  - ip: 192.168.2.15
    pass: '00000'
    port: 22
    devel-su: '00000'
"""

    @staticmethod
    def _get_path_conf(path, default):

        path = get_path_file(path, False)
        default = get_path_file(default, False)

        if path and os.path.isfile(path) and path.lower().endswith('.yaml'):
            return Path(path)
        else:
            if not os.path.isfile(default):
                Conf._create_default_config(default)
            return Path(default)

    @staticmethod
    def _create_default_config(path):
        if not click.confirm(AppTexts.conf_confirm()):
            exit(0)

        path_dir = os.path.dirname(path)

        # Create dir if not exist
        if not os.path.isdir(path_dir):
            Path(path_dir).mkdir()

        # Write default configuration file
        with open(path, 'w') as file:
            print(Conf._get_default_config(), file=file)

        echo_stdout(AppTexts.conf_created_success(path), 2)

    @staticmethod
    def _check_key_pairs(path: Path):
        path_dir = Path(os.path.dirname(path)) / 'keys'
        if not path_dir.is_dir():
            # Create a folder immediately to ask 1 time
            path_dir.mkdir()
            if click.confirm(AppTexts.conf_download_keys_confirm()):
                echo_stdout(AppTexts.loading())
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
                # Echo info success
                echo_stdout(AppTexts.conf_download_keys_success(str(path_dir)), 2)

    def __init__(self, path):
        # Get path config
        self.conf_path = Conf._get_path_conf(path, default=PATH_CONF)

        # Check and download key pairs
        Conf._check_key_pairs(self.conf_path)

        # Load config
        with open(self.conf_path, 'rb') as file:
            self.conf = load(file.read(), Loader=Loader)

    # Get config path
    def get_path(self) -> Path:
        return self.conf_path

    # Get config keys
    def get_type_output(self, verbose: bool) -> VerboseType:
        if verbose:
            return VerboseType.verbose
        if 'output' not in self.conf.keys():
            return VerboseType.short
        match self.conf['output']:
            case 'short':
                return VerboseType.short
            case 'command':
                return VerboseType.command
            case 'verbose':
                return VerboseType.verbose
        return VerboseType.short

    # Get config keys
    def get_keys(self) -> {}:
        keys = {}
        # If empty
        if 'keys' not in self.conf.keys():
            return keys
        # Format keys
        for item in self.conf['keys']:
            # Check data
            if not item['name'] or not item['key'] or not item['cert']:
                click.echo('{} {}'.format(
                    click.style('The configuration file is filled in incorrectly:', fg='red'), self.conf_path))
                exit(1)
            keys[str(item['name'])] = {
                'name': str(item['name']),
                'key': str(item['key']),
                'cert': str(item['cert']),
            }
        return keys

    # Get config devices
    def get_devices(self) -> {}:
        devices = {}
        # If empty
        if 'devices' not in self.conf.keys():
            return devices
        # Format keys
        for item in self.conf['devices']:
            # Check data
            if not item['ip'] or not item['pass'] or not item['port'] or not item['devel-su']:
                click.echo('{} {}'.format(
                    click.style('The configuration file is filled in incorrectly:', fg='red'), self.conf_path))
                exit(1)
            devices[str(item['ip'])] = {
                'ip': str(item['ip']),
                'pass': str(item['pass']),
                'port': str(item['port']),
                'devel-su': str(item['devel-su']),
            }
        return devices
