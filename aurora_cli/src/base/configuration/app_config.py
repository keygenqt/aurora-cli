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

from aurora_cli.src.base.configuration.loader_config import ConfigLoader
from aurora_cli.src.base.constants.config import DEFAULT_CONFIG, PATH_CONFIG
from aurora_cli.src.base.helper import convert_relative_path
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.sign_package_model import SignPackageModel
from aurora_cli.src.base.output import echo_stdout, echo_stdout_json, OutResultError, echo_stdout_with_check
from aurora_cli.src.base.texts.error import TextError


class AppConfig:
    def __init__(self, _data_config: {}):
        self._data_config = _data_config
        self._commands_verbose_save = []

    @staticmethod
    def create_test():
        return AppConfig(ConfigLoader(
            default_config=DEFAULT_CONFIG
        ).get_data())

    @staticmethod
    def create(path: str | None, is_api: bool):
        if path is not None and not convert_relative_path(path).is_file():
            echo_stdout_with_check(is_api, OutResultError(TextError.validate_config_arg_path(path)))
            exit(1)
        try:
            loader = ConfigLoader(
                default_config=DEFAULT_CONFIG,
                path=convert_relative_path(path),
                default_path=convert_relative_path(PATH_CONFIG),
                stdout=lambda out: echo_stdout(out)
            )
        except (Exception,):
            echo_stdout_with_check(is_api, OutResultError(TextError.config_arg_path_load_error(
                path=path if path else PATH_CONFIG
            )))
            exit(1)
        if loader.is_error():
            if is_api:
                echo_stdout_json(OutResultError(
                    message=TextError.validate_config_error(),
                    value=loader.get_validate_json()
                ))
            else:
                echo_stdout(TextError.validate_config_error())
                for output in loader.get_validate():
                    echo_stdout(output, prefix='- ')
            exit(1)
        return AppConfig(loader.get_data())

    def get_workdir(self) -> Path | None:
        return Path(self._data_config['workdir'])

    def get_keys(self) -> []:
        keys = []
        for item in self._data_config['keys']:
            keys.append(SignPackageModel(
                name=item['name'],
                key=Path(item['key']),
                cert=Path(item['cert']),
            ))
        return keys

    def get_devices(self) -> []:
        devices = []
        for item in self._data_config['devices']:
            devices.append(DeviceModel(
                host=item['host'],
                port=item['port'],
                auth=item['auth'],
                devel_su=item['devel-su'],
            ))
        return devices

    def add_verbose_map(self, command: str, stdout: [], stderr: []):
        self._commands_verbose_save.append({
            'command': command,
            'stdout': stdout,
            'stderr': stderr,
        })

    def seize_verbose_map(self):
        data = self._commands_verbose_save
        self._commands_verbose_save = []
        return data
