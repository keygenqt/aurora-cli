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
import os.path
from pathlib import Path

from yaml import Loader
from yaml import load

from aurora_cli.src.base.configuration_check import CheckConfiguration
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.sign_package_model import SignPackageModel


class AppConfiguration:

    def __init__(self, path):
        # Get path config
        self.conf_path = path
        # Load config
        with open(self.conf_path, 'rb') as file:
            self.loader = load(file.read(), Loader=Loader)

    def get_keys(self) -> []:
        result = CheckConfiguration.check_keys(self.loader)
        if result.is_error():
            return []
        keys = []
        for item in self.loader['keys']:
            keys.append(SignPackageModel(
                name=item['name'],
                key=Path(item['key']),
                cert=Path(item['cert']),
            ))
        return keys

    def get_devices(self) -> []:
        result = CheckConfiguration.check_devices(self.loader)
        if result.is_error():
            return []
        devices = []
        for item in self.loader['devices']:
            if os.path.isfile(item['auth']):
                item['auth'] = Path(item['auth'])
            devices.append(DeviceModel(
                host=item['host'],
                port=item['port'],
                auth=item['auth'],
                devel_su=item['devel-su'],
            ))
        return devices
