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

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import click
from paramiko.client import SSHClient

from aurora_cli.src.base.common.features.ssh_features import ssh_get_device_platform_name, ssh_get_device_platform_arch
from aurora_cli.src.base.interface.model_client import ModelClient
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import OutResult, OutResultError, echo_stdout
from aurora_cli.src.base.utils.prompt import prompt_model_select
from aurora_cli.src.base.utils.ssh import ssh_client_connect


@dataclass
class DeviceModel(ModelClient):
    """Class device."""
    host: str
    port: int
    auth: Any
    devel_su: Any = None
    user: str = 'defaultuser'

    @staticmethod
    def get_model_select(
            select: bool,
            index: Any,
    ) -> OutResult:
        return prompt_model_select(
            name='device',
            models=[model.host for model in DeviceModel.get_models_list()],
            select=select,
            index=index,
        )

    @staticmethod
    def get_model_by_host(host: str):
        try:
            models = DeviceModel.get_models_list()
            list_index = [model.host for model in models].index(host)
            return models[list_index]
        except (Exception,):
            echo_stdout(OutResultError(TextError.device_not_found_error(host)))
            app_exit()

    @staticmethod
    @click.pass_context
    def get_models_list(ctx: {}) -> []:
        return ctx.obj.get_devices()

    def get_host(self) -> str:
        return self.host

    def get_port(self) -> int:
        return self.port

    def get_pass(self) -> Any:
        if self.is_password():
            return self.auth
        return None

    def get_device_info(self):
        platform_name = 'AuroraOS-unknown'
        platform_arch = 'aurora-arm'

        result = self.get_ssh_client()
        if result.is_error():
            return platform_name, platform_arch

        _name = ssh_get_device_platform_name(result.value, close=False)
        _arch = ssh_get_device_platform_arch(result.value, close=True)

        if _name is not None:
            platform_name = f'AuroraOS-{_name}'
        if _arch is not None:
            platform_arch = _arch

        # @todo fix for 3.16.2-2
        # return platform_name, platform_arch
        return platform_name, None

    def get_ssh_key(self) -> Any:
        if self.is_password():
            return None
        return self.auth

    def is_password(self) -> bool:
        return type(self.auth) is str

    def get_ssh_client(self) -> Any:
        client = ssh_client_connect(
            self.host,
            self.user,
            self.port,
            self.auth
        )
        if not client:
            return OutResultError(TextError.ssh_connect_device_error())
        else:
            return OutResult(value=client)

    def to_dict(self) -> dict:
        return {
            'host': self.host,
            'port': self.port,
            'auth': str(self.auth),
            'devel_su': self.devel_su if self.devel_su else False,
            'user': self.user,
        }
