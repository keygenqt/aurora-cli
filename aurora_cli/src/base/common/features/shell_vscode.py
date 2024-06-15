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
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.shell import shell_exec_command


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

    version = stdout[-1].split(' ')[2]

    return OutResult(TextSuccess.vscode_extension_install_success(version))
