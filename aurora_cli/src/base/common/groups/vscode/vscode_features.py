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
from pathlib import Path
from typing import Any

from aurora_cli.src.base.common.features.shell_vscode import shell_vscode_list_extensions, \
    shell_vscode_extension_install, shell_vscode_version
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.output import echo_stdout, OutResultInfo
from aurora_cli.src.base.utils.tests import tests_exit


def vscode_version_common():
    return shell_vscode_version()


def vscode_extensions_list_common() -> list:
    return shell_vscode_list_extensions()


def vscode_extensions_flutter_check_common(extensions: Any = None) -> list:
    if extensions is None:
        extensions = shell_vscode_list_extensions()
    install = []
    for extension in [
        'dart-code.dart-code',
        'dart-code.flutter',
    ]:
        if extension not in extensions:
            install.append(extension)
    return install


def vscode_extensions_cpp_check_common(extensions: Any = None) -> list:
    if extensions is None:
        extensions = shell_vscode_list_extensions()
    install = []
    for extension in [
        'mesonbuild.mesonbuild',
        'ms-vscode.cmake-tools',
        'ms-vscode.cpptools',
        'ms-vscode.cpptools-extension-pack',
        'ms-vscode.cpptools-themes',
        'twxs.cmake',
        'webfreak.debug',
    ]:
        if extension not in extensions:
            install.append(extension)
    return install


def vscode_extensions_other_check_common(extensions: Any = None) -> list:
    if extensions is None:
        extensions = shell_vscode_list_extensions()
    install = []
    for extension in [
        'streetsidesoftware.code-spell-checker',
        'streetsidesoftware.code-spell-checker-russian',
        'ybaumes.highlight-trailing-white-spaces',
    ]:
        if extension not in extensions:
            install.append(extension)
    return install


def vscode_extensions_install(extensions: list):
    tests_exit()
    for extension in extensions:
        echo_stdout(OutResultInfo(TextInfo.vscode_extensions_installing(extension)))
        result = shell_vscode_extension_install(extension)
        echo_stdout(result)


def vscode_settings_common():
    tests_exit()
    is_update = False
    extensions = shell_vscode_list_extensions()
    path_folder = Path.home() / '.config' / 'Code' / 'User'
    path_config = path_folder / 'settings.json'

    if not path_folder.is_dir():
        path_folder.mkdir(parents=True)

    if not path_config.is_file():
        path_config.write_text('{}')

    with open(path_config, 'r+') as file:
        fcntl.lockf(file, fcntl.LOCK_EX)
        config = json.loads(file.read())

        if 'streetsidesoftware.code-spell-checker-russian' in extensions:
            if 'cSpell.language' not in config.keys():
                config['cSpell.language'] = 'en,ru'
                is_update = True

        if 'files.insertFinalNewline' not in config.keys():
            config['files.insertFinalNewline'] = True
            is_update = True

        if 'files.trimFinalNewlines' not in config.keys():
            config['files.trimFinalNewlines'] = True
            is_update = True

        if is_update:
            file.seek(0)
            file.write(json.dumps(config, indent=2, ensure_ascii=False))
            file.truncate()

    if is_update:
        echo_stdout(OutResultInfo(TextInfo.vscode_settings_update(str(path_config))))
    else:
        echo_stdout(OutResultInfo(TextInfo.vscode_settings_not_update()))
