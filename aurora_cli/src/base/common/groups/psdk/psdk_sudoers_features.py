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

import getpass
import subprocess
from pathlib import Path

from aurora_cli.src.base.constants.other import (
    MER_SDK_CHROOT_PATH,
    SDK_CHROOT_PATH,
    MER_SDK_CHROOT_DATA,
    SDK_CHROOT_DATA
)
from aurora_cli.src.base.models.psdk_model import PsdkModel
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import echo_stdout, OutResultInfo, OutResult
from aurora_cli.src.base.utils.shell import shell_exec_command
from aurora_cli.src.base.utils.tests import tests_exit
from aurora_cli.src.base.utils.text_file import (
    file_exist_in_line,
    file_permissions_777,
    file_permissions_644,
    file_remove_line
)


def shell_auth_sudo(password, model):
    if model and psdk_is_sudoers(model):
        return True
    try:
        subprocess.check_output('echo {} | sudo -S echo -n'.format(password if password else 'undefined'),
                                stderr=subprocess.STDOUT,
                                timeout=1,
                                shell=True)
        return True
    except (Exception,):
        return False


def psdk_is_sudoers(model: PsdkModel):
    path = Path(MER_SDK_CHROOT_PATH)
    tool = Path(model.get_tool_path())
    if not path.is_file():
        return False
    if file_exist_in_line(path, str(tool.parent)):
        return True
    else:
        return False


def psdk_sudoers_add_common(
        model: PsdkModel,
        password = None
):
    tests_exit()
    for item in [[MER_SDK_CHROOT_PATH, MER_SDK_CHROOT_DATA], [SDK_CHROOT_PATH, SDK_CHROOT_DATA]]:
        path = Path(item[0])
        tool = Path(model.get_tool_path())
        user = getpass.getuser()
        data = item[1].format(username=user, psdk_tool=tool, psdk_tool_folder=tool.parent)
        if not path.is_file():
            shell_exec_command(['sudo', 'touch', str(path)], password=password)
        if file_exist_in_line(path, str(tool.parent)):
            echo_stdout(OutResultInfo(TextInfo.psdk_sudoers_exist(model.version, str(path))))
        else:
            file_permissions_777(path, password=password)
            with open(path, 'a') as file:
                file.write(data)
            file_permissions_644(path, password=password)
            echo_stdout(OutResult(TextSuccess.psdk_sudoers_add_success(model.version, str(path))))


def psdk_sudoers_remove_common(
        model: PsdkModel,
        password = None
):
    tests_exit()
    for path in [MER_SDK_CHROOT_PATH, SDK_CHROOT_PATH]:
        path = Path(path)
        tool = Path(model.get_tool_path())
        if not path.is_file():
            echo_stdout(OutResultInfo(TextInfo.psdk_sudoers_not_found(model.version, str(path))))
            continue
        if not file_exist_in_line(path, str(tool.parent)):
            echo_stdout(OutResultInfo(TextInfo.psdk_sudoers_not_found(model.version, str(path))))
            continue
        file_permissions_777(path, password=password)
        file_remove_line(path, str(tool.parent))
        file_permissions_644(path, password=password)
        echo_stdout(OutResult(TextSuccess.psdk_sudoers_remove_success(model.version, str(path))))
