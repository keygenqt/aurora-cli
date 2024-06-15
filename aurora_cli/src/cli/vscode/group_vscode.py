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

import click

from aurora_cli.src.base.common.groups.vscode.vscode_features import (
    vscode_extensions_flutter_check_common,
    vscode_extensions_list_common,
    vscode_extensions_cpp_check_common,
    vscode_extensions_install,
    vscode_extensions_other_check_common,
    vscode_settings_common
)
from aurora_cli.src.base.configuration.app_config import AppConfig
from aurora_cli.src.base.texts.app_argument import TextArgument
from aurora_cli.src.base.texts.app_command import TextCommand
from aurora_cli.src.base.texts.app_group import TextGroup
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.prompt import TextPrompt
from aurora_cli.src.base.utils.output import echo_verbose, OutResultInfo, echo_stdout


@click.group(name='vscode', help=TextGroup.group_vscode())
def group_vscode():
    AppConfig.create_test()


@group_vscode.command(name='tuning', help=TextCommand.command_vscode_tuning())
@click.option('-v', '--verbose', is_flag=True, help=TextArgument.argument_verbose())
def tuning(verbose: bool):
    extensions = vscode_extensions_list_common()

    # Flutter
    install = vscode_extensions_flutter_check_common(extensions)
    if install:
        echo_stdout(OutResultInfo(TextInfo.vscode_extensions_flutter(install)))
        if click.confirm(TextPrompt.select_continue()):
            vscode_extensions_install(install)
    else:
        echo_stdout(OutResultInfo(TextInfo.vscode_extensions_flutter_installed()))

    # C++
    install = vscode_extensions_cpp_check_common(extensions)
    if install:
        echo_stdout(OutResultInfo(TextInfo.vscode_extensions_cpp(install)))
        if click.confirm(TextPrompt.select_continue()):
            vscode_extensions_install(install)
    else:
        echo_stdout(OutResultInfo(TextInfo.vscode_extensions_cpp_installed()))

    # Common
    install = vscode_extensions_other_check_common(extensions)
    if install:
        echo_stdout(OutResultInfo(TextInfo.vscode_extensions_other(install)))
        if click.confirm(TextPrompt.select_continue()):
            vscode_extensions_install(install)
    else:
        echo_stdout(OutResultInfo(TextInfo.vscode_extensions_other_installed()))

    # Default configration VS Code
    vscode_settings_common()

    echo_verbose(verbose)
