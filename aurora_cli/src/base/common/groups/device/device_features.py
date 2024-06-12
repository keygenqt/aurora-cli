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

from aurora_cli.src.base.common.groups.common.ssh_commands import (
    ssh_command_common,
    ssh_upload_common
)
from aurora_cli.src.base.models.device_model import DeviceModel


def device_command_common(
        model: DeviceModel,
        execute: str,
        verbose: bool
): ssh_command_common(model, execute, verbose)


def device_upload_common(
        model: DeviceModel,
        path: str,
        verbose: bool
): ssh_upload_common(model, path, verbose)