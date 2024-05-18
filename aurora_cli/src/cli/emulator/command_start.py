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

from aurora_cli.src.base.common.output import echo_stdout, echo_stderr, echo_verbose_shell
from aurora_cli.src.base.common.texts.error import TextError
from aurora_cli.src.base.common.texts.info import TextInfo
from aurora_cli.src.base.common.texts.success import TextSuccess
from aurora_cli.src.base.shell import ResultExec
from aurora_cli.src.common.emulator.features import emulator_start


@click.group(name='start', invoke_without_command=True)
@click.option('-v', '--verbose', is_flag=True, help='Command output')
def command_start(verbose: bool):
    """Start emulator."""
    match emulator_start():
        case ResultExec.success:
            echo_stdout(TextSuccess.emulator_start_success())
        case ResultExec.locked:
            echo_stdout(TextInfo.emulator_start_locked())
        case ResultExec.error:
            echo_stderr(TextError.emulator_start_error())
    if verbose:
        echo_verbose_shell()
