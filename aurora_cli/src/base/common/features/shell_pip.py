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
from aurora_cli.src.base.constants.app import APP_NAME, APP_VERSION
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.shell import shell_exec_command


@check_dependency(DependencyApps.pip)
def shell_pip_versions() -> []:
    stdout, stderr = shell_exec_command([
        'pip',
        'index',
        'versions',
        APP_NAME,
    ])
    if stderr:
        return OutResultError(TextError.get_data_error())

    latest = 'undefined'

    for line in stdout:
        if 'Available' in line:
            version = line.split(',')[0].split(' ')[-1].split('.')
            if len(version) == 4:
                latest = '.'.join(version[:-1])
            else:
                latest = '.'.join(version)

    return OutResult(value={
        'INSTALLED': APP_VERSION,
        'LATEST': latest,
    })
