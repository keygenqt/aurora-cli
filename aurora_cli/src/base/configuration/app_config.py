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
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.argv import argv_is_api
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResult
from aurora_cli.src.base.utils.path import path_convert_relative


class AppConfig:
    def __init__(self, _data_config: {}):
        self._data_config = _data_config

    @staticmethod
    def create_test():
        return AppConfig(ConfigLoader(CONFIG_DEFAULT).get_data())

    @staticmethod
    def create(path: str | None):
        arg_path = path_convert_relative(path)
        default_path = path_convert_relative(CONFIG_PATH)
        try:
            def load_file_config(config_path: Path) -> AnyStr:
                with open(config_path, 'rb') as file_config:
                    return file_config.read()

            if arg_path is not None:
                if not arg_path.is_file():
                    echo_stdout(OutResultError(TextError.validate_config_arg_path(path)))
                    exit(1)
                else:
                    config_str = load_file_config(arg_path)
            else:
                if not default_path.is_file():
                    default_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(default_path, 'w') as file:
                        print(CONFIG_DEFAULT, file=file)
                    echo_stdout(OutResult(TextInfo.create_default_config_file(str(default_path))))
                    config_str = CONFIG_DEFAULT
                else:
                    config_str = load_file_config(default_path)

            loader = ConfigLoader(config_str)
        except (Exception,):
            echo_stdout(OutResultError(TextError.config_arg_path_load_error(
                path=path if path else CONFIG_PATH
            )))
            exit(1)
        if loader.is_error():
            if argv_is_api():
                echo_stdout(OutResultError(
                    message=TextError.validate_config_error(),
                    value=loader.get_validate_json()
                ))
            else:
                echo_stdout(TextError.validate_config_error())
                for output in loader.get_validate():
                    echo_stdout(output, prefix='- ')
            exit(1)
        return AppConfig(loader.get_data())

    def get_workdir(self) -> str | None:
        return self._data_config['workdir']

    def get_keys(self) -> []:
        keys = []
        for item in self._data_config['keys']:
            keys.append(SignModel(
                name=item['name'],
                key=Path(item['key']),
                cert=Path(item['cert']),
            ))
        return keys

    def get_devices(self) -> []:
        devices = []
        for item in self._data_config['devices']:
            path_file = path_convert_relative(item['auth'])
            if path_file and path_file.is_file():
                item['auth'] = path_file
            devices.append(DeviceModel(
                host=item['host'],
                port=item['port'],
                auth=item['auth'],
                devel_su=item['devel-su'],
            ))
        return devices
