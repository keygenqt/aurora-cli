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
from bs4 import BeautifulSoup

from aurora_cli.src.base.texts.info import TextInfo


# Json output codes
class EchoJsonCode(Enum):
    info = 100
    success = 200
    error = 500


@dataclass
class OutResult:
    """Class out data."""
    message: str = None
    value: any = None
    index: int = None
    code: EchoJsonCode = EchoJsonCode.success

    def is_error(self):
        return self.code != EchoJsonCode.success


@dataclass
class OutResultError(OutResult):
    """Class out data EchoJsonCode.Bad_Request."""
    code: EchoJsonCode = EchoJsonCode.error


@dataclass
class OutResultInfo(OutResult):
    """Class out data EchoJsonCode.Not_Found."""
    code: EchoJsonCode = EchoJsonCode.info


# Color tags
class EchoColors(Enum):
    red = 'red'
    green = 'green'
    yellow = 'yellow'
    blue = 'blue'
    magenta = 'magenta'
    cyan = 'cyan'
    white = 'white'
    reset = 'reset'


# App output echo
def echo_stdout(
        out: OutResult | str | None,
        verbose: bool = False,
        newlines: int = 1
):
    if type(out) is str:
        click.echo(_colorize_text(out))
    else:
        if out.message:
            click.echo(_colorize_text(out.message).strip(), nl=False)
            for x in range(newlines):
                click.echo()
        if not out.message and out.value:
            click.echo(out.value)
    if verbose:
        echo_verbose_shell()


def echo_stdout_json(out: OutResult | None, verbose: bool = False):
    _echo_stdout_json(out, verbose)


@click.pass_context
def _echo_stdout_json(ctx: {}, out: OutResult | None, verbose: bool = False):
    if out:
        data = {
            'code': out.code.value,
        }
        if out.message is not None:
            data['message'] = _colorize_clear(out.message).strip()
        if out.value is not None:
            data['value'] = out.value
        if out.index is not None:
            data['index'] = out.index
        if verbose:
            data['verbose'] = ctx.obj.seize_verbose_map()
        click.echo(json.dumps(data, indent=2))


def echo_verbose_shell():
    _echo_verbose_shell()


@click.pass_context
def _echo_verbose_shell(ctx: {}):
    for exec_command in ctx.obj.seize_verbose_map():
        echo_stdout(OutResult(TextInfo.command_execute(exec_command['command'])))
        if exec_command['stdout']:
            echo_stdout(OutResult('\n'.join(exec_command['stdout'])))
        if exec_command['stderr']:
            echo_stdout(OutResult('\n'.join(exec_command['stderr'])))


# App output echo just line
def echo_line(newlines: int = 1):
    for x in range(newlines):
        click.echo()


# Colorize text clear
def _colorize_clear(text: str) -> str:
    if '<' not in text:
        return text
    soup = BeautifulSoup(text, 'html.parser')
    for tag in EchoColors:
        for item in soup.findAll(tag.value):
            text = text.replace('<{}>{}</{}>'.format(tag.value, item.text, tag.value), item.text)
    return text


# Colorize text by tags
def _colorize_text(text: str) -> str:
    if '<' not in text:
        return text
    soup = BeautifulSoup(text, 'html.parser')
    for tag in EchoColors:
        for item in soup.findAll(tag.value):
            text = text.replace(
                '<{}>{}</{}>'.format(tag.value, item.text, tag.value),
                click.style(item.text, fg=tag.value))
    return click.style(text, fg='reset')
