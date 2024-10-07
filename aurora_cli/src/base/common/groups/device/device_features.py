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

from aurora_cli.src.base.common.features.shell_features import shell_ssh_copy_id
from aurora_cli.src.base.common.groups.common.ssh_commands import ssh_command_common, ssh_upload_common, ssh_info_common
from aurora_cli.src.base.models.device_model import DeviceModel
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResultInfo, OutResult


def device_info_common(
        model: DeviceModel,
): ssh_info_common(model, False)


def device_command_common(
        model: DeviceModel,
        execute: str,
): ssh_command_common(model, execute)


def device_upload_common(
        model: DeviceModel,
        path: str,
): ssh_upload_common(model, path)


def device_ssh_copy_id_common(
        model: DeviceModel,
):
    if model.is_password():
        echo_stdout(OutResultError(TextError.ssh_copy_id_without_key()))
        app_exit(1)

    echo_stdout(OutResultInfo(TextInfo.ssh_copy_id_password()))
    echo_stdout(shell_ssh_copy_id(model.host, model.auth))
