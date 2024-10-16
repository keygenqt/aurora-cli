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
from typing import Any

from aurora_cli.src.base.constants.other import VM_MANAGE
from aurora_cli.src.base.interface.model_client import ModelClient
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError, echo_stdout
from aurora_cli.src.base.utils.shell import shell_exec_command
from aurora_cli.src.base.utils.ssh import ssh_client_connect


@dataclass
class EmulatorModel(ModelClient):
    """Class emulator."""
    name: str
    path: Path
    is_on: bool
    is_record: bool
    host: str = 'localhost'
    user: str = 'defaultuser'
    port: int = 2223

    @staticmethod
    def get_model_user():
        name, path, is_on, is_record = EmulatorModel._get_arg()
        return EmulatorModel(name, path, is_on, is_record)

    @staticmethod
    def get_model_root():
        name, path, is_on, is_record = EmulatorModel._get_arg()
        return EmulatorModel(name, path, is_on, is_record, user='root')

    @staticmethod
    def get_models_list() -> []:
        name = EmulatorModel._vm_emulator_name()
        if not name:
            return []
        return [EmulatorModel.get_model_user()]

    @staticmethod
    def _get_arg():
        name = EmulatorModel._vm_emulator_name()
        info = EmulatorModel._vm_emulator_info(name)
        if not name or not info['info_path']:
            echo_stdout(OutResultError(TextError.emulator_not_found()))
            app_exit()
        return name, info['info_path'], EmulatorModel._vm_emulator_is_on(name), info['is_record']

    def get_host(self) -> str:
        return '127.0.0.1'

    def get_port(self) -> int:
        return self.port

    def get_pass(self) -> Any:
        return None

    def get_emulator_info(self):
        platform_name = self.name.replace('-base', '')
        platform_arch = 'aurora-x64'

        # @todo fix for 3.16.2-2
        # return platform_name, platform_arch
        return platform_name, None

    def get_ssh_key(self) -> Any:
        return self.path.parent.parent.parent / 'vmshare' / 'ssh' / 'private_keys' / 'sdk'

    def is_password(self) -> bool:
        return False

    def get_ssh_client(self) -> Any:
        if not self.is_on:
            return OutResultError(TextError.emulator_not_found_running())
        client = ssh_client_connect(
            self.host,
            self.user,
            self.port,
            self.get_ssh_key()
        )
        if not client:
            return OutResultError(TextError.ssh_connect_emulator_error())
        else:
            return OutResult(value=client)

    @staticmethod
    @check_dependency(DependencyApps.vboxmanage)
    def _vm_emulator_name() -> Any:
        stdout, stderr = shell_exec_command([
            VM_MANAGE,
            'list',
            'vms',
        ])
        if stderr:
            return None
        for line in stdout:
            if 'AuroraOS' in line:
                return line.split('"')[1]
        return None

    @staticmethod
    @check_dependency(DependencyApps.vboxmanage)
    def _vm_emulator_is_on(emulator_name: Any) -> bool:
        if not emulator_name:
            return False
        stdout, stderr = shell_exec_command([
            VM_MANAGE,
            'list',
            'runningvms',
        ])
        for line in stdout:
            if emulator_name in line:
                return True
        return False

    @staticmethod
    @check_dependency(DependencyApps.vboxmanage)
    def _vm_emulator_info(emulator_name: str) -> {}:
        info_path = None
        is_record = False

        if not emulator_name:
            return None
        stdout, stderr = shell_exec_command([
            VM_MANAGE,
            'showvminfo',
            emulator_name,
        ])

        for line in stdout:
            if 'Snapshot folder:' in line:
                info_path = Path(os.path.dirname(line.replace('Snapshot folder:', '').strip()))
            if 'Recording enabled:' in line and 'yes' in line:
                is_record = True
        return {
            'info_path': info_path,
            'is_record': is_record,
        }
