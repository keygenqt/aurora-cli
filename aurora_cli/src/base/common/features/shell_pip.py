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

from aurora_cli.src.base.constants.app import APP_NAME, APP_VERSION
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult


@check_dependency(DependencyApps.pip)
def shell_pip_versions() -> []:
    latest = 'undefined'
    try:
        stdout = (subprocess.check_output('pip index versions {}'.format(APP_NAME),
                                          stderr=subprocess.STDOUT,
                                          timeout=3,
                                          shell=True)
                  .decode('utf-8')
                  .split('\n'))
        for line in stdout:
            if 'Available' in line:
                version = line.split(',')[0].split(' ')[-1].split('.')
                if len(version) == 4:
                    latest = '.'.join(version[:-1])
                else:
                    latest = '.'.join(version)
    except (Exception,):
        pass

    return OutResult(value={
        'INSTALLED': APP_VERSION,
        'LATEST': latest,
    })
