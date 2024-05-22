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


# Check dependency vscode plugin
def check_dependency_vscode_plugin(name: str) -> bool:
    output = subprocess.check_output(['code', '--list-extensions']).decode('utf-8')
    if name in output:
        return True
    return False


# Check dependency apt
def check_dependency_apt() -> bool:
    try:
        subprocess.run(['apt', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (Exception,):
        return False


# Check dependency sshpass
def check_dependency_sshpass() -> bool:
    try:
        subprocess.run(['sshpass', '-V'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (Exception,):
        return False
