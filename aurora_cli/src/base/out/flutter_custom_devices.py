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
from pathlib import Path


def gen_custom_device(
        key: str,
        ip: str,
        port: int,
        ssh_key: Path,
        platform_name: str,
        platform_arch: str
) -> {}:
    return {
        'id': f'custom-aurora-{ip}',
        'label': key,
        'sdkNameAndVersion': platform_name,
        'platform': platform_arch,
        'enabled': True,
        'ping': ['nc', '-w', '3', '-vz', ip, str(port)],
        'pingSuccessRegex': None,
        'postBuild': None,
        'install': ['echo'],
        'uninstall': ['echo'],
        'runDebug': ['echo'],
        'forwardPort': [
            'ssh',
            '-i',
            str(ssh_key),
            f'-p{port}',
            '-o',
            'BatchMode=yes',
            '-o',
            'ExitOnForwardFailure=yes',
            '-L',
            '127.0.0.1:${hostPort}:127.0.0.1:${devicePort}',
            f'defaultuser@{ip}',
            'echo \'Port forwarding success\'; read'
        ],
        'forwardPortSuccessRegex': 'Port forwarding success',
        'screenshot': None
    }
