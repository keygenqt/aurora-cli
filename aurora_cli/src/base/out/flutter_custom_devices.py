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


def gen_custom_device(
        device_id: str,
        device_ip: str,
) -> {}:
    return {
        'id': device_id,
        'label': f'Aurora ({device_id})',
        'sdkNameAndVersion': 'Aurora 4/5',
        'platform': None,
        'enabled': True,
        'ping': [
            'python3',
            '/home/keygenqt/Documents/Home/Projects/aurora-cli/builds/aurora-cli-3.0.0.pyz',
            'emulator',
            'command',
            '--execute',
            'version'
        ],
        'pingSuccessRegex': None,
        'postBuild': None,
        'install': [
            'scp',
            '-r',
            '-o',
            'BatchMode=yes',
            '${localPath}',
            'defaultuser@192.168.2.15:/tmp/${appName}'
        ],
        'uninstall': [
            'ssh',
            '-o',
            'BatchMode=yes',
            'defaultuser@192.168.2.15',
            'rm -rf "/tmp/${appName}"'
        ],
        'runDebug': [
            'ssh',
            '-o',
            'BatchMode=yes',
            'defaultuser@192.168.2.15',
            'flutter-pi /tmp/${appName}'
        ],
        'forwardPort': [
            'ssh',
            '-o',
            'BatchMode=yes',
            '-o',
            'ExitOnForwardFailure=yes',
            '-L',
            '127.0.0.1:${hostPort}:127.0.0.1:${devicePort}',
            'defaultuser@192.168.2.15',
            'echo \'Port forwarding success\'; read'
        ],
        'forwardPortSuccessRegex': 'Port forwarding success',
        'screenshot': None
    }
