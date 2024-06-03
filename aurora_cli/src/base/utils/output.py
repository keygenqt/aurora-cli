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

import json
from dataclasses import dataclass
from enum import Enum

import click

from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.argv import argv_is_api
from aurora_cli.src.base.utils.text import text_colorize_clear, text_colorize
from aurora_cli.src.base.utils.verbose import verbose_seize_map


class EchoJsonCode(Enum):
    info = 100
    success = 200
    error = 500


@dataclass
class OutResult:
    message: str = None
    value: any = None
    index: int = None
    code: EchoJsonCode = EchoJsonCode.success

    def is_error(self):
        return self.code == EchoJsonCode.error

    def to_json(self):
        data = {
            'code': self.code.value
        }
        if self.message:
            data['message'] = text_colorize_clear(self.message)
        if self.value:
            data['value'] = self.value
        if self.index:
            data['index'] = self.index
        return data


@dataclass
class OutResultError(OutResult):
    code: EchoJsonCode = EchoJsonCode.error


@dataclass
class OutResultInfo(OutResult):
    code: EchoJsonCode = EchoJsonCode.info


def echo_stdout(
        out: OutResult | str | None,
        verbose: bool = False,
        newlines: int = 1,
        prefix: str = '',
):
    if out:
        if argv_is_api():
            _echo_stdout_json(out, verbose)
        else:
            _echo_stdout_shell(out, verbose, newlines, prefix)


def _echo_stdout_shell(
        out: OutResult | str | None,
        verbose: bool = False,
        newlines: int = 1,
        prefix: str = ''
):
    if out is not None:
        if type(out) is str:
            click.echo(prefix + text_colorize(out))
        else:
            if out.message:
                click.echo(prefix + text_colorize(out.message).strip(), nl=False)
                for x in range(newlines):
                    click.echo()
            if not out.message and out.value:
                click.echo(out.value)
    if verbose:
        for exec_command in verbose_seize_map():
            echo_stdout(OutResult(TextInfo.command_execute(exec_command['command'])))
            if exec_command['stdout']:
                echo_stdout(OutResult('\n'.join(exec_command['stdout'])))
            if exec_command['stderr']:
                echo_stdout(OutResult('\n'.join(exec_command['stderr'])))


def _echo_stdout_json(
        out: OutResult | None,
        verbose: bool = False
):
    if out:
        data = out.to_json()
        if verbose:
            data['verbose'] = verbose_seize_map()
        click.echo(json.dumps(data, indent=2, ensure_ascii=False))
