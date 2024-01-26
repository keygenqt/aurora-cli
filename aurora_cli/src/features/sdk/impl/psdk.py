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
import subprocess
from pathlib import Path

import click
from cffi.backend_ctypes import unicode

# Sudoers chroot mer-sdk-chroot
MER_SDK_CHROOT = '/etc/sudoers.d/mer-sdk-chroot'
MER_SDK_CHROOT_DATA = '''{username} ALL=(ALL) NOPASSWD: {psdk_dir}
Defaults!{psdk_dir} env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"
'''

# Sudoers chroot sdk-chroot
SDK_CHROOT = '/etc/sudoers.d/sdk-chroot'
SDK_CHROOT_DATA = '''{username} ALL=(ALL) NOPASSWD: {psdk_dir}/sdk-chroot
Defaults!{psdk_dir}/sdk-chroot env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"
'''


# Get list installed psdk
def get_list_psdk_installed():
    results = {}
    folders = [folder for folder in os.listdir(Path.home()) if
               os.path.isdir(Path.home() / folder) and 'Platform' in folder and os.path.isfile(
                   Path.home() / folder / 'sdks' / 'aurora_psdk' / 'sdk-chroot')]
    for folder in folders:
        results[folder] = str(Path.home() / folder / 'sdks' / 'aurora_psdk' / 'sdk-chroot')
    return results


# Check is add psdk sudoers and run sudo query
def check_sudoers_chroot(psdk_key):
    if os.path.isfile(SDK_CHROOT):
        with open(SDK_CHROOT) as f:
            if psdk_key in f.read():
                return

    subprocess.call(['sudo', 'echo', '-n'])


# Get list psdk targets
def get_list_targets(chroot):
    targets = []
    with subprocess.Popen([
        chroot,
        'sdk-assistant',
        'list',
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        for line in iter(lambda: process.stdout.readline(), ""):
            if not line:
                break
            line = unicode(line.rstrip(), "utf-8")
            if '─' in line and 'default' not in line:
                targets.append(line[2:])

    return targets
