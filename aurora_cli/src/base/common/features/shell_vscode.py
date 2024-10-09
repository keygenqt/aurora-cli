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
import fcntl
import json
import subprocess
from pathlib import Path

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.shell import shell_exec_command


def shell_vscode_version():
    try:
        result = subprocess.run(['code', '--version'], capture_output=True)
        return {'VERSION': result.stdout.decode("utf-8").split('\n')[0]}
    except (Exception,):
        return {'VERSION': 'undefined'}


@check_dependency(DependencyApps.vscode)
def shell_vscode_list_extensions() -> []:
    stdout, stderr = shell_exec_command([
        'code',
        '--list-extensions',
    ])
    if stderr:
        return []
    return stdout


@check_dependency(DependencyApps.vscode)
def shell_vscode_extension_install(extension: str) -> OutResult:
    stdout, stderr = shell_exec_command([
        'code',
        '--install-extension',
        extension
    ])
    if stderr and 'successfully' not in stdout[-1]:
        return OutResultError(TextError.vscode_extension_install_error())

    try:
        version = stdout[-1].split(' ')[2]
        return OutResult(TextSuccess.vscode_extension_install_success(version))
    except (Exception,):
        return OutResult(TextSuccess.vscode_extension_install_success())


def update_launch_debug_dart(
        url: str,
        project: Path
):
    project_path = project
    if (project_path / 'example').is_dir():
        project_path = project / 'example'

    path_folder = project_path / '.vscode'
    path_launch = path_folder / 'launch.json'

    if not path_folder.is_dir():
        path_folder.mkdir(parents=True, exist_ok=True)

    if not path_launch.is_file():
        path_launch.write_text('{}')

    with open(path_launch, 'r+') as file:
        fcntl.lockf(file, fcntl.LOCK_EX)
        launch = json.loads(file.read())
        configurations = [
            {
                'name': 'Flutter Aurora OS Dart Debug',
                'type': 'dart',
                'request': 'attach',
                'vmServiceUri': url,
                'program': 'lib/main.dart' if project_path == project else 'example/lib/main.dart',
            }
        ]

        if 'configurations' in launch.keys():
            for item in launch['configurations']:
                if 'Flutter Aurora OS Dart Debug' != item['name']:
                    configurations.append(item)

        launch['configurations'] = configurations

        file.seek(0)
        file.write(json.dumps(launch, indent=2, ensure_ascii=False))
        file.truncate()


@check_dependency(DependencyApps.gdb_multiarch)
def update_launch_debug_gdb(
        host: str,
        binary: str,
        package: str,
        project: Path,
):
    project_path = project
    if (project_path / 'example').is_dir():
        project_path = project / 'example'

    path_folder = project_path / '.vscode'
    path_launch = path_folder / 'launch.json'
    path_gdbinit = project_path / '.gdbinit'

    if not path_folder.is_dir():
        path_folder.mkdir(parents=True, exist_ok=True)

    if not path_launch.is_file():
        path_launch.write_text('{}')

    with open(path_gdbinit, 'w') as file:
        print(f'handle SIGILL pass nostop noprint\n'
              f'set remote exec-file /usr/bin/{package}', file=file)

    with open(path_launch, 'r+') as file:
        fcntl.lockf(file, fcntl.LOCK_EX)
        launch = json.loads(file.read())
        configurations = [
            {
                'name': 'Flutter Aurora OS GDB Debug',
                'type': 'cppdbg',
                'request': 'launch',
                'program': binary,
                'MIMode': 'gdb',
                'miDebuggerPath': '/usr/bin/gdb-multiarch',
                'miDebuggerServerAddress': f'{host}:2345',
                'useExtendedRemote': True,
                'cwd': '${workspaceRoot}',
            }
        ]

        if 'configurations' in launch.keys():
            for item in launch['configurations']:
                if 'Flutter Aurora OS GDB Debug' != item['name']:
                    configurations.append(item)

        launch['configurations'] = configurations

        file.seek(0)
        file.write(json.dumps(launch, indent=2, ensure_ascii=False))
        file.truncate()
