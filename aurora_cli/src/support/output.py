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
from enum import Enum

import click
from bs4 import BeautifulSoup


# Verbose output types
class VerboseType(Enum):
    short = 'Short output'
    command = 'Show output with command'
    verbose = 'Show output command'
    none = 'Disable all output'


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


# App output echo just line
def echo_line(newlines: int = 1):
    for x in range(newlines):
        click.echo()


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
