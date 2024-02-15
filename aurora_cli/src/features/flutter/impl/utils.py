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
from pathlib import Path

GDBINIT_DATA = '''handle SIGILL pass nostop noprint
set remote exec-file /usr/bin/{package}'''

GDBVSCODE_DATA = r'''{{
    "version": "0.2.0",
    "configurations": [
        {{
            "name": "Attach with GDB",
            "type": "cppdbg",
            "request": "launch",
            "program": "{rmp_path}",
            "MIMode": "gdb",
            "miDebuggerPath": "/usr/bin/gdb-multiarch",
            "miDebuggerServerAddress": "{ip}:{port}",
            "useExtendedRemote": true,
            "cwd": "${{workspaceRoot}}"
         }}
    ]
}}'''


# Get list installed flutter
def get_list_flutter_installed() -> []:
    path = Path.home() / '.local' / 'opt'
    folders = [folder for folder in os.listdir(path) if os.path.isdir(path / folder)
               and 'flutter-' in folder
               and os.path.isfile(path / folder / 'bin' / 'flutter')]
    folders.sort(reverse=True)
    return [v.replace('flutter-', '') for v in folders]


# Get keys form spec file
# Name
# Version
# Release
def get_spec_keys(file: Path) -> [None, None, None]:
    result = [None, None, None]
    if not file.is_file():
        return [None, None, None]
    with open(file, 'r') as file:
        for line in file:
            if 'Name:' in line:
                result[0] = line.replace('Name: ', '').strip()
            if 'Version:' in line:
                result[1] = line.replace('Version: ', '').strip()
            if 'Release:' in line:
                result[2] = line.replace('Release: ', '').strip()
    return result
