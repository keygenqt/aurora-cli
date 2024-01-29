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


# Get installed sdk
def get_sdk_installed():
    folders = [folder for folder in os.listdir(Path.home()) if
               os.path.isdir(Path.home() / folder) and 'Aurora' in folder and os.path.isfile(
                   Path.home() / folder / 'sdk-release')]
    if folders:
        with open(Path.home() / folders[0] / 'sdk-release') as f:
            return [
                'Aurora SDK: {}'.format(f.readline().strip().split('=')[1].replace('-base', '')),
                str(Path.home() / folders[0])
            ]
    return [None, None]
