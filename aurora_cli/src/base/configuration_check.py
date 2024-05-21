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

from aurora_cli.src.base.helper import convert_relative_path
from aurora_cli.src.base.output import OutResult, OutResultError
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess


class CheckConfiguration:
    @staticmethod
    def check_keys(loader: {}) -> OutResult:
        # Check exist
        if 'keys' not in loader.keys():
            return OutResultError(TextError.validate_config_keys_not_found())
        # Check values
        for item in loader['keys']:
            if 'name' not in item or 'key' not in item or 'cert' not in item:
                return OutResultError(TextError.validate_config_keys())
        # Check files
        for item in loader['keys']:
            if not os.path.isfile(convert_relative_path(item['key'])):
                return OutResultError(TextError.validate_config_key_not_found(item['key']))
            if not os.path.isfile(convert_relative_path(item['cert'])):
                return OutResultError(TextError.validate_config_cert_not_found(item['cert']))
        return OutResult(TextSuccess.validate_config_keys())

    @staticmethod
    def check_devices(loader: {}) -> OutResult:
        # Check exist
        if 'devices' not in loader.keys():
            return OutResultError(TextError.validate_config_devices_not_found())
        # Check values
        for item in loader['devices']:
            if 'host' not in item or 'port' not in item or 'auth' not in item or 'devel-su' not in item:
                return OutResultError(TextError.validate_config_devices())
        return OutResult(TextSuccess.validate_config_devices())
