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

from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.models.sign_model import SignModel
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout


def cli_psdk_tool_select_model_psdk(
        select: bool,
        index: Any,
) -> PsdkModel:
    result_model = PsdkModel.get_model_select(select, index)
    if result_model.is_error():
        echo_stdout(result_model)
        app_exit()
    return PsdkModel.get_model_by_version(result_model.value)


def cli_psdk_tool_select_target_psdk(model: PsdkModel) -> str:
    result_target = model.get_model_targets_select()
    if not result_target.is_success():
        echo_stdout(result_target)
        app_exit()
    return result_target.value


def cli_psdk_tool_select_model_sign(
        select: bool,
        index: Any,
) -> Any:
    result_model = SignModel.get_model_select(select, index)
    if result_model.is_error():
        return None
    return SignModel.get_model_by_name(result_model.value)
