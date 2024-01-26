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

from cffi.backend_ctypes import unicode


# Get emulator Aurora SDK virtualbox
def get_emulator_vm():
    try:
        output, error = subprocess.Popen([
            'VBoxManage',
            'list',
            'vms',
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        emulator = [vm for vm in unicode(output.rstrip(), "utf-8").split('\n') if 'AuroraOS' in vm]

        if not emulator:
            return [None, None]

        return (emulator[0]
                .replace('"', '')
                .replace('{', '')
                .replace('}', '')
                .split(' '))
    except FileNotFoundError:
        pass

    return [None, None]


# Startup vm virtualbox
def run_emulator_vm(key):
    subprocess.Popen([
        'VBoxManage',
        'startvm',
        key,
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
