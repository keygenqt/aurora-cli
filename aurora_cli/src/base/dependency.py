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
import subprocess
from enum import Enum

from aurora_cli.src.base.constants.other import VM_MANAGE
from aurora_cli.src.base.output import OutResult, OutResultError
from aurora_cli.src.base.texts.error import TextError


class ShellApps(Enum):
    vboxmanage = VM_MANAGE
    ffmpeg = 'ffmpeg'
    sudo = 'sudo'
    git = 'git'
    ssh = 'ssh'


def check_dependency(key: str) -> OutResult:
    match key:
        case ShellApps.vboxmanage.value:
            return check_dependency_vboxmanage()
        case ShellApps.ffmpeg.value:
            return check_dependency_ffmpeg()
        case ShellApps.sudo.value:
            return check_dependency_sudo()
        case ShellApps.git.value:
            return check_dependency_git()
        case ShellApps.ssh.value:
            return check_dependency_ssh()
    return OutResult()


def check_dependency_vboxmanage() -> OutResult:
    try:
        subprocess.run([VM_MANAGE, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return OutResult()
    except (Exception,):
        return OutResultError(TextError.dependency_not_found('VBoxManage'))


def check_dependency_ffmpeg() -> OutResult:
    try:
        subprocess.run(['ffmpeg', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return OutResult()
    except (Exception,):
        return OutResultError(TextError.dependency_not_found('ffmpeg'))


def check_dependency_sudo() -> OutResult:
    try:
        subprocess.run(['sudo', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return OutResult()
    except (Exception,):
        return OutResultError(TextError.dependency_not_found('sudo'))


def check_dependency_git() -> OutResult:
    try:
        subprocess.run(['git', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return OutResult()
    except (Exception,):
        return OutResultError(TextError.dependency_not_found('git'))


def check_dependency_ssh() -> OutResult:
    try:
        subprocess.run(['ssh', '-V'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return OutResult()
    except (Exception,):
        return OutResultError(TextError.dependency_not_found('ssh'))
