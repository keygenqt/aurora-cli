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
from typing import AnyStr

from aurora_cli.src.base.configuration.loader_config import ConfigLoader
from aurora_cli.src.base.constants.config import CONFIG_DEFAULT, CONFIG_PATH
from aurora_cli.src.base.helper import convert_relative_path, convert_relative_path_check
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.sign_package_model import SignPackageModel
from aurora_cli.src.base.output import echo_stdout, OutResultError, OutResult
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo


class AppConfig:
    def __init__(self, _data_config: {}, _is_api: bool):
        self._is_api = _is_api
        self._data_config = _data_config
        self._commands_verbose_save = []

    @staticmethod
    def create_test(is_api: bool = False):
        return AppConfig(ConfigLoader(CONFIG_DEFAULT).get_data(), is_api)

    @staticmethod
    def create(path: str | None, is_api: bool):
        arg_path = convert_relative_path(path)
        default_path = convert_relative_path(CONFIG_PATH)
        try:
            def load_file_config(config_path: Path) -> AnyStr:
                with open(config_path, 'rb') as file_config:
                    return file_config.read()

            if arg_path is not None:
                if not arg_path.is_file():
                    echo_stdout(OutResultError(TextError.validate_config_arg_path(path)), is_api=is_api)
                    exit(1)
                else:
                    config_str = load_file_config(arg_path)
            else:
                if not default_path.is_file():
                    default_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(default_path, 'w') as file:
                        print(CONFIG_DEFAULT, file=file)
                    echo_stdout(OutResult(TextInfo.create_default_config_file(str(default_path))), is_api=is_api)
                    config_str = CONFIG_DEFAULT
                else:
                    config_str = load_file_config(default_path)

            loader = ConfigLoader(config_str)
        except (Exception,):
            echo_stdout(OutResultError(TextError.config_arg_path_load_error(
                path=path if path else CONFIG_PATH
            )), is_api=is_api)
            exit(1)
        if loader.is_error():
            if is_api:
                echo_stdout(OutResultError(
                    message=TextError.validate_config_error(),
                    value=loader.get_validate_json()
                ), is_api=True)
            else:
                echo_stdout(TextError.validate_config_error())
                for output in loader.get_validate():
                    echo_stdout(output, prefix='- ')
            exit(1)
        return AppConfig(loader.get_data(), is_api)

    def is_api(self) -> bool:
        return self._is_api

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
                auth=convert_relative_path_check(item['auth']),
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
