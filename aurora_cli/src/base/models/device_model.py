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
from dataclasses import dataclass
from pathlib import Path

import click
from paramiko.client import SSHClient

from aurora_cli.src.base.output import OutResult, OutResultError
from aurora_cli.src.base.ssh import ssh_client_connect
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.cli.helper import model_select


@dataclass
class DeviceModel:
    """Class device."""
    host: str
    port: int
    auth: str | Path
    devel_su: str | None = None
    user: str = 'defaultuser'

    @staticmethod
    def get_model_select(select: bool, index: int | None) -> OutResult:
        return model_select(
            models=DeviceModel.get_lists_devices(),
            select=select,
            index=index
        )

    @staticmethod
    def get_model(host: str, port: int, auth: str, devel_su: str = None):
        if os.path.isfile(auth):
            auth = Path(auth)
        return DeviceModel(host, port, auth, devel_su)

    @staticmethod
    @click.pass_context
    def get_lists_devices(ctx: {}) -> []:
        return ctx.obj.get_devices()

    @staticmethod
    def get_names_devices() -> []:
        return [obj.host for obj in DeviceModel.get_lists_devices()]

    def get_ssh_client(self) -> SSHClient | OutResult:
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
