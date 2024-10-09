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
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.output import OutResultError, echo_stdout


class DependencyApps(Enum):
    vboxmanage = VM_MANAGE
    ffmpeg = 'ffmpeg'
    sudo = 'sudo'
    git = 'git'
    ssh = 'ssh'
    clang_format = 'clang-format'
    tar = 'tar'
    vscode = 'vscode'
    gdb_multiarch = 'gdb-multiarch'
    pip = 'pip'


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
        if app == DependencyApps.vboxmanage:
            _check_dependency_vboxmanage()
        elif app == DependencyApps.ffmpeg:
            _check_dependency_ffmpeg()
        elif app == DependencyApps.sudo:
            _check_dependency_sudo()
        elif app == DependencyApps.git:
            _check_dependency_git()
        elif app == DependencyApps.ssh:
            _check_dependency_ssh()
        elif app == DependencyApps.clang_format:
            _check_dependency_clang_format()
        elif app == DependencyApps.tar:
            _check_dependency_tar()
        elif app == DependencyApps.vscode:
            _check_dependency_vscode()
        elif app == DependencyApps.gdb_multiarch:
            _check_dependency_gdb_multiarch()
        elif app == DependencyApps.pip:
            _check_dependency_pip()


def _check_dependency_vboxmanage():
    try:
        subprocess.run([VM_MANAGE, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('VBoxManage')))
        app_exit()


def _check_dependency_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('ffmpeg')))
        app_exit()


def _check_dependency_sudo():
    try:
        subprocess.run(['sudo', '-V'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('sudo')))
        app_exit()


def _check_dependency_git():
    try:
        subprocess.run(['git', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('git')))
        app_exit()


def _check_dependency_ssh():
    try:
        subprocess.run(['ssh', '-V'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('ssh')))
        app_exit()


def _check_dependency_clang_format():
    try:
        subprocess.run(['clang-format', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('clang-format')))
        app_exit()


def _check_dependency_tar():
    try:
        subprocess.run(['tar', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('tar')))
        app_exit()


def _check_dependency_vscode():
    try:
        subprocess.run(['code', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('vscode')))
        app_exit()


def _check_dependency_gdb_multiarch():
    try:
        subprocess.run(['gdb-multiarch', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('gdb-multiarch')))
        app_exit()


def _check_dependency_pip():
    try:
        subprocess.run(['pip', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stdout(OutResultError(TextError.dependency_not_found('pip')))
        app_exit()
