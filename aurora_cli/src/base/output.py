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

from aurora_cli.src.base.common.texts.info import TextInfo
from aurora_cli.src.base.shell import shell_verbose_map


# Json output codes
class EchoJsonCode(Enum):
    # The application cannot or will not process the request due to something that is perceived to be a client error.
    Bad_Request = 400
    # The application cannot find the requested resource.
    Not_Found = 404
    # The application refuses the attempt to brew coffee with a teapot.
    Im_teapot = 418
    # The application has encountered a situation it does not know how to handle.
    Internal_Server_Error = 500
    # The request succeeded.
    OK = 200


@dataclass
class Out:
    """Class out data."""
    message: str
    data: str = None
    code: EchoJsonCode = EchoJsonCode.OK


@dataclass
class Out400(Out):
    """Class out data EchoJsonCode.Bad_Request."""
    code: EchoJsonCode = EchoJsonCode.Bad_Request


@dataclass
class Out404(Out):
    """Class out data EchoJsonCode.Not_Found."""
    code: EchoJsonCode = EchoJsonCode.Not_Found


@dataclass
class Out418(Out):
    """Class out data EchoJsonCode.Im_teapot."""
    code: EchoJsonCode = EchoJsonCode.Im_teapot


@dataclass
class Out500(Out):
    """Class out data EchoJsonCode.Internal_Server_Error."""
    code: EchoJsonCode = EchoJsonCode.Internal_Server_Error


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
def echo_stdout(out: Out, verbose: bool = False, newlines: int = 1):
    if out.message:
        click.echo(_colorize_text(out.message).strip(), nl=False)
        for x in range(newlines):
            click.echo()
    if verbose:
        echo_verbose_shell()


# App output echo json
def echo_stdout_json(out: Out, verbose: bool = False):
    data = {
        'code': out.code.value,
        'message': _colorize_clear(out.message).strip(),
    }
    if out.data:
        data['data'] = out.data
    if verbose:
        data['verbose'] = shell_verbose_map()
    click.echo(json.dumps(data, indent=2))


def echo_verbose_shell():
    for exec_command in shell_verbose_map():
        echo_stdout(Out(TextInfo.command_execute(exec_command['command'])))
        if exec_command['stdout']:
            echo_stdout(Out('\n'.join(exec_command['stdout'])))
        if exec_command['stderr']:
            echo_stdout(Out('\n'.join(exec_command['stderr'])))


# App output echo just line
def echo_line(newlines: int = 1):
    for x in range(newlines):
        click.echo()


# App output echo json EchoJsonCode.Bad_Request
def echo_stdout_json_400(out: Out):
    echo_stdout_json(out)


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
