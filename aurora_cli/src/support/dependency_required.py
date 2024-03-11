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

from aurora_cli.src.support.output import echo_stderr
from aurora_cli.src.support.texts import AppTexts


# Check dependency for init
def check_dependency_init():
    try:
        subprocess.run(['git', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_git())
        exit(1)
    try:
        subprocess.run(['sudo', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_sudo())
        exit(1)


# Check dependency ffmpeg
def check_dependency_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_ffmpeg())
        exit(1)


# Check dependency vscode
def check_dependency_vscode():
    try:
        subprocess.run(['code', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_vscode())
        exit(1)


# Check dependency gdb-multiarch
def check_dependency_gdb_multiarch():
    try:
        subprocess.run(['gdb-multiarch', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_gdb_multiarch())
        exit(1)
