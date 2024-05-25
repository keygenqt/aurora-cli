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

from paramiko.client import SSHClient

from aurora_cli.src.base.common.vm_features import vm_emulator_ssh_key
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.ssh import ssh_client_connect
from aurora_cli.src.base.texts.error import TextError


@dataclass
class EmulatorModel:
    """Class emulator."""
    host: str = 'localhost'
    user: str = 'defaultuser'
    port: int = 2223

    @staticmethod
    def get_model_user():
        return EmulatorModel()

    @staticmethod
    def get_model_root():
        return EmulatorModel(user='root')

    def get_ssh_client(self) -> SSHClient | OutResult:
        # Get path to key
        result = vm_emulator_ssh_key()
        if result.is_error():
            return result
        # Get ssh client
        client = ssh_client_connect(
            self.host,
            self.user,
            self.port,
            result.value
        )
        if not client:
            return OutResultError(TextError.ssh_connect_emulator_error())
        else:
            return OutResult(value=client)
