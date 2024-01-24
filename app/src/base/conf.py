import os
from pathlib import Path

import click.exceptions
from yaml import Loader
from yaml import load


# Loader configuration yaml
class Conf:
    def __init__(self, path):

        # Get path config
        if path is not None and os.path.isfile(path) and path.lower().endswith('.yaml'):
            self.conf_path = Path(path)
        else:
            self.conf_path = Path(os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.realpath(__file__)))))) / "configuration.yaml"

        # Load config
        if self.conf_path.is_file():
            with open(self.conf_path, 'rb') as file:
                self.conf = load(file.read(), Loader=Loader)
        else:
            click.echo('{} {}'.format(click.style('Configuration file not found:', fg='red'), self.conf_path))
            exit(1)

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
