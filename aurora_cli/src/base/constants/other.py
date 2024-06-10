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

VM_MANAGE = "VBoxManage"

MER_SDK_CHROOT_PATH = '/etc/sudoers.d/mer-sdk-chroot'
MER_SDK_CHROOT_DATA = ('{username} ALL=(ALL) NOPASSWD: {psdk_tool_folder}\n'
                       'Defaults!{psdk_tool_folder} env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"\n')

SDK_CHROOT_PATH = '/etc/sudoers.d/sdk-chroot'
SDK_CHROOT_DATA = ('{username} ALL=(ALL) NOPASSWD: {psdk_tool}\n'
                   'Defaults!{psdk_tool} env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"\n')
