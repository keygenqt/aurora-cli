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
from typing import Any

from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout


def cli_device_tool_select_model(
        select: bool,
        index: Any,
) -> DeviceModel:
    result_model = DeviceModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model)
        app_exit()
    return DeviceModel.get_model_by_host(result_model.value)
