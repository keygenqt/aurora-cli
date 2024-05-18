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


# App output echo error
def echo_stderr(text: str, newlines: int = 1):
    if text:
        click.echo(_colorize_text(text).strip(), nl=False, err=True)
        for x in range(newlines):
            click.echo()


# App output echo
def echo_stdout(text: str, newlines: int = 1):
    if text:
        click.echo(_colorize_text(text).strip(), nl=False)
        for x in range(newlines):
            click.echo()


# App output echo json
def echo_stdout_json(message: str, verbose: bool = False, code: EchoJsonCode = EchoJsonCode.OK):
    data = {
        'code': code.value,
        'message': _colorize_clear(message).strip(),
    }
    if verbose:
        data['verbose'] = shell_verbose_map()
    click.echo(json.dumps(data, indent=2))


def echo_verbose_shell():
    for exec_command in shell_verbose_map():
        echo_stdout(TextInfo.command_execute(exec_command['command']))
        if exec_command['stdout']:
            echo_stdout('\n'.join(exec_command['stdout']))
        if exec_command['stderr']:
            echo_stdout('\n'.join(exec_command['stderr']))


# App output echo just line
def echo_line(newlines: int = 1):
    for x in range(newlines):
        click.echo()


# App output echo json EchoJsonCode.Bad_Request
def echo_stdout_json_400(message: str, verbose: bool = False):
    echo_stdout_json(
        message=message,
        verbose=verbose,
        code=EchoJsonCode.Bad_Request
    )


# App output echo json EchoJsonCode.Not_Found
def echo_stdout_json_404(message: str, verbose: bool = False):
    echo_stdout_json(
        message=message,
        verbose=verbose,
        code=EchoJsonCode.Not_Found
    )


# App output echo json EchoJsonCode.Im_teapot
def echo_stdout_json_418(message: str, verbose: bool = False):
    echo_stdout_json(
        message=message,
        verbose=verbose,
        code=EchoJsonCode.Im_teapot
    )


# App output echo json EchoJsonCode.Internal_Server_Error
def echo_stdout_json_500(message: str, verbose: bool = False):
    echo_stdout_json(
        message=message,
        verbose=verbose,
        code=EchoJsonCode.Internal_Server_Error
    )


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
