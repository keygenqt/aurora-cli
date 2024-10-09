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

from aurora_cli.src.base.common.features.shell_pip import shell_pip_versions
from aurora_cli.src.base.common.groups.psdk.psdk_sudoers_features import shell_auth_sudo
from aurora_cli.src.base.constants.app import APP_VERSION, PATH_DIR
from aurora_cli.src.base.constants.config import CONFIG_PATH
from aurora_cli.src.base.utils.output import OutResult
from aurora_cli.src.base.utils.path import path_convert_relative


def app_info_common():
    return OutResult(value={
        'VERSION': APP_VERSION,
        'PATH_CONFIG': f'{path_convert_relative(CONFIG_PATH)}',
        'PATH_FOLDER': f'{path_convert_relative(PATH_DIR)}',
    })


def app_versions_common():
    return shell_pip_versions()


def app_auth_check_common(model):
    return OutResult(value=shell_auth_sudo(password=None, model=model))


def app_auth_password_common(password):
    return OutResult(value=shell_auth_sudo(password=password, model=None))
