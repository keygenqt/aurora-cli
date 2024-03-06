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
import json
import os
from pathlib import Path

import click

from aurora_cli.src.features.flutter.impl.utils import get_list_flutter_installed
from aurora_cli.src.support.helper import prompt_index, pc_command
from aurora_cli.src.support.output import echo_stdout, echo_stderr, VerboseType, echo_line
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.versions import get_flutter_plugins


@click.group(name='plugins', invoke_without_command=True)
def group_flutter_plugins():
    """Get types plugins info."""

    available_plugins_list = get_flutter_plugins()
    available_plugins_list = [plugin.split('-')[0].replace('_aurora', '') for plugin in available_plugins_list]

    # Required flutter
    flutters = get_list_flutter_installed()
    if not flutters:
        echo_stderr(AppTexts.flutter_not_found())
        exit(0)

    # Select flutter
    echo_stdout(AppTexts.select_versions(flutters))
    echo_stdout(AppTexts.array_indexes(flutters), 2)
    flutter = Path.home() / '.local' / 'opt' / 'flutter-{}'.format(flutters[prompt_index(flutters)]) / 'bin' / 'flutter'

    # Enable custom device in flutter
    pc_command([
        flutter,
        'pub',
        'get',
    ], VerboseType.none, [], True)

    json_conf = Path(os.getcwd()) / '.dart_tool' / 'package_config.json'

    with open(json_conf, 'r') as file:
        data = json.loads(file.read())

    if not data and not data['packages']:
        echo_stderr(AppTexts.flutter_error_read_json())
        exit(0)

    platform_specific_plugins = []
    not_platform_specific_plugins = []
    aurora_platform_specific_plugins = []

    keys = [
        '_android',
        '_ios',
        '_linux',
        '_macos',
        '_web',
        '_windows',
        '_aurora'
    ]

    def if_has_key(name: str, value: []):
        for key in keys:
            if name.replace(key, '') in value:
                return True
        return False

    for item in data['packages']:
        plugin = Path(item['rootUri'].replace('file://', '')) / 'pubspec.yaml'
        if plugin.is_file():
            with open(plugin, 'r') as file:
                if file.read().find("platforms:") == -1:
                    if not if_has_key(item['name'], not_platform_specific_plugins):
                        not_platform_specific_plugins.append(item['name'])
                else:
                    has_pd = if_has_key(item['name'], platform_specific_plugins)
                    has_ar = if_has_key(item['name'], aurora_platform_specific_plugins)
                    if not has_pd and not has_ar:
                        if item['name'] in available_plugins_list:
                            aurora_platform_specific_plugins.append(item['name'])
                        else:
                            platform_specific_plugins.append(item['name'])

    echo_stdout(AppTexts.flutter_platform_specific_plugins_has_aurora(aurora_platform_specific_plugins))
    echo_line(1 if (len(platform_specific_plugins)) else 0)
    echo_stdout(AppTexts.flutter_platform_specific_plugins(platform_specific_plugins))
    echo_line(1 if (len(not_platform_specific_plugins)) else 0)
    echo_stdout(AppTexts.flutter_platform_not_specific_plugins(not_platform_specific_plugins))
