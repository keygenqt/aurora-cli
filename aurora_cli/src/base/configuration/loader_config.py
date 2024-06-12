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

from typing import AnyStr

from yaml import load, Loader

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.path import path_convert_relative


class ConfigLoader:
    def __init__(self, config: AnyStr):
        self._result_checks = []
        self._loader = load(config, Loader=Loader)

    def get_data(self):
        return self._loader

    def get_validate(self) -> []:
        if not self._result_checks:
            self._result_checks = [self._check_workdir(), self._check_keys(), self._check_devices()]
        return self._result_checks

    def get_validate_json(self):
        return [result.to_map() for result in self.get_validate()]

    def is_error(self):
        for result in self.get_validate():
            if result.is_error():
                return True
        return False

    def _check_workdir(self) -> OutResult:
        # Check exist
        if self._loader is None or 'workdir' not in self._loader.keys():
            return OutResultError(TextError.validate_config_workdir_not_found())
        # Check value
        path = path_convert_relative(self._loader['workdir'])
        path.mkdir(parents=True, exist_ok=True)
        if not path.is_dir():
            return OutResultError(TextError.validate_config_workdir_error_create(self._loader['workdir']))

        return OutResult(TextSuccess.validate_config_workdir())

    def _check_keys(self) -> OutResult:
        # Check exist
        if self._loader is None or 'keys' not in self._loader.keys():
            return OutResultError(TextError.validate_config_keys_not_found())
        # Check values
        for item in self._loader['keys']:
            if 'name' not in item or 'key' not in item or 'cert' not in item:
                return OutResultError(TextError.validate_config_keys())
        # Check files
        for item in self._loader['keys']:
            if not path_convert_relative(item['key']).is_file():
                return OutResultError(TextError.validate_config_key_not_found(item['key']))
            if not path_convert_relative(item['cert']).is_file():
                return OutResultError(TextError.validate_config_cert_not_found(item['cert']))
        return OutResult(TextSuccess.validate_config_keys())

    def _check_devices(self) -> OutResult:
        # Check exist
        if self._loader is None or 'devices' not in self._loader.keys():
            return OutResultError(TextError.validate_config_devices_not_found())
        # Check values
        for item in self._loader['devices']:
            if 'host' not in item or 'port' not in item or 'auth' not in item or 'devel-su' not in item:
                return OutResultError(TextError.validate_config_devices())
        return OutResult(TextSuccess.validate_config_devices())
