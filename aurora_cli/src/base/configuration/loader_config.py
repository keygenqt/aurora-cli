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

from pathlib import Path
from typing import Callable

from yaml import load, Loader

from aurora_cli.src.base.helper import convert_relative_path
from aurora_cli.src.base.output import OutResult, OutResultError
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess


class ConfigLoader:
    def __init__(
            self,
            default_config: str,
            path: Path | None = None,
            default_path: Path | None = None,
            stdout: Callable[[OutResult], None] = None,
    ):
        if default_path is None:
            self._loader = load(default_config, Loader=Loader)
        else:
            if path is None and not default_path.is_file():
                default_path.parent.mkdir(parents=True, exist_ok=True)
                with open(default_path, 'w') as file:
                    print(default_config, file=file)
                self._loader = load(default_config, Loader=Loader)
                if stdout:
                    stdout(OutResult(TextInfo.create_default_config_file(str(default_path))))
            else:
                with open(path if path else default_path, 'rb') as file:
                    self._loader = load(file.read(), Loader=Loader)

        self.result_checks = []
        self.result_checks.append(self._check_workdir())
        self.result_checks.append(self._check_keys())
        self.result_checks.append(self._check_devices())

    def get_data(self):
        return self._loader

    def get_validate(self):
        return self.result_checks

    def get_validate_json(self):
        return [result.to_json() for result in self.result_checks]

    def is_error(self):
        for result in self.result_checks:
            if result.is_error():
                return True
        return False

    def _check_workdir(self) -> OutResult:
        # Check exist
        if 'workdir' not in self._loader.keys():
            return OutResultError(TextError.validate_config_workdir_not_found())
        # Check value
        path = convert_relative_path(self._loader['workdir'])
        path.mkdir(parents=True, exist_ok=True)
        if not path.is_dir():
            return OutResultError(TextError.validate_config_workdir_error_create(self._loader['workdir']))

        return OutResult(TextSuccess.validate_config_workdir())

    def _check_keys(self) -> OutResult:
        # Check exist
        if 'keys' not in self._loader.keys():
            return OutResultError(TextError.validate_config_keys_not_found())
        # Check values
        for item in self._loader['keys']:
            if 'name' not in item or 'key' not in item or 'cert' not in item:
                return OutResultError(TextError.validate_config_keys())
        # Check files
        for item in self._loader['keys']:
            if not convert_relative_path(item['key']).is_file():
                return OutResultError(TextError.validate_config_key_not_found(item['key']))
            if not convert_relative_path(item['cert']).is_file():
                return OutResultError(TextError.validate_config_cert_not_found(item['cert']))
        return OutResult(TextSuccess.validate_config_keys())

    def _check_devices(self) -> OutResult:
        # Check exist
        if 'devices' not in self._loader.keys():
            return OutResultError(TextError.validate_config_devices_not_found())
        # Check values
        for item in self._loader['devices']:
            if 'host' not in item or 'port' not in item or 'auth' not in item or 'devel-su' not in item:
                return OutResultError(TextError.validate_config_devices())
        return OutResult(TextSuccess.validate_config_devices())
