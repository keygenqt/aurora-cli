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
import functools
import subprocess
from enum import Enum

from aurora_cli.src.base.constants.other import VM_MANAGE
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.output import OutResultError, echo_stdout


class DependencyApps(Enum):
    vboxmanage = VM_MANAGE
    ffmpeg = 'ffmpeg'
    sudo = 'sudo'
    git = 'git'
    ssh = 'ssh'


def check_dependency(*apps: DependencyApps):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            _check_dependency(*apps)
            return function(*args, **kwargs)

        return wrapper

    return decorator


def _check_dependency(*apps: DependencyApps):
    for app in apps:
        match app:
            case DependencyApps.vboxmanage:
                _check_dependency_vboxmanage()
            case DependencyApps.ffmpeg:
                _check_dependency_ffmpeg()
            case DependencyApps.sudo:
                _check_dependency_sudo()
            case DependencyApps.git:
                _check_dependency_git()
            case DependencyApps.ssh:
                _check_dependency_ssh()


def _check_dependency_vboxmanage():
    try:
        subprocess.run([VM_MANAGE, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('VBoxManage')))
        exit(1)


def _check_dependency_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('ffmpeg')))
        exit(1)


def _check_dependency_sudo():
    try:
        subprocess.run(['sudo', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('sudo')))
        exit(1)


def _check_dependency_git():
    try:
        subprocess.run(['git', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('git')))
        exit(1)


def _check_dependency_ssh():
    try:
        subprocess.run(['ssh', '-V'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('ssh')))
        exit(1)
